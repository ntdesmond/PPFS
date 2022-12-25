import asyncio
from bson import ObjectId
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

from ..models.dataclasses import User
from ..exceptions.auth import InvalidCredentialsError, UserNotFoundError
from ..models.schemas import UserAuthentication
from ..settings import UserConfig, settings


class Users:
    def __init__(self, database: str = "ppfs", collection: str = "users"):
        client = AsyncIOMotorClient(
            host=settings.mongodb.host,
            username=settings.mongodb.username,
            password=settings.mongodb.password,
        )
        self.__collection = client[database][collection]
        self.__password_context = CryptContext(schemes=["bcrypt"])

        asyncio.run_coroutine_threadsafe(
            self.__create_index(), loop=asyncio.get_running_loop()
        )

    async def __create_index(self):
        await self.__collection.create_index("username", unique=True)

    async def authenticate(self, user_auth: UserAuthentication) -> User:
        user = await self.__collection.find_one({"username": user_auth.username})

        if user is None or not self.__password_context.verify(
            user_auth.password, user["password"]
        ):
            raise InvalidCredentialsError("Invalid username or password.")

        user["id"] = user["_id"]
        return User.parse_obj(user)

    async def create(self, user_auth: UserAuthentication, is_admin: bool) -> User:
        try:
            result = await self.__collection.insert_one(
                {
                    "username": user_auth.username,
                    "password": self.__password_context.hash(user_auth.password),
                    "is_admin": is_admin,
                }
            )
        except DuplicateKeyError:
            raise InvalidCredentialsError("Username is already taken.")
        return User(
            id=result.inserted_id, username=user_auth.username, is_admin=is_admin
        )

    async def create_default(self, user: UserConfig) -> None:
        try:
            await self.create(UserAuthentication.parse_obj(user), user.is_admin)
        except InvalidCredentialsError:
            pass

    async def clear(self) -> None:
        await self.__collection.drop()

    async def get(self, id: ObjectId) -> User:
        user = await self.__collection.find_one({"_id": id})

        if user is None:
            raise UserNotFoundError("User not found.")

        user["id"] = user["_id"]
        return User.parse_obj(user)
