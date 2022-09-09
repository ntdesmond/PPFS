import asyncio

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError

from ..exceptions.auth import InvalidCredentialsError, UserNotFoundError
from ..models.dataclasses import User, UserRole
from ..models.schemas import UserAuthentication
from ..settings import settings


class Users:
    def __init__(self, database: str = "ppfs", collection: str = "users"):
        client = AsyncIOMotorClient(
            host=settings.mongodb_host,
            username=settings.mongodb_username,
            password=settings.mongodb_password,
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

    async def create(self, user_auth: UserAuthentication, role: UserRole) -> User:
        try:
            result = await self.__collection.insert_one(
                {
                    "username": user_auth.username,
                    "password": self.__password_context.hash(user_auth.password),
                    "role": role.value,
                }
            )
        except DuplicateKeyError:
            raise InvalidCredentialsError("Username is already taken.")
        return User(id=result.inserted_id, username=user_auth.username, role=role)

    async def create_default_superuser(self, user_auth: UserAuthentication) -> None:
        try:
            await self.create(user_auth, UserRole.SUPERUSER)
        except InvalidCredentialsError:
            pass

    async def get(self, id: ObjectId) -> User:
        user = await self.__collection.find_one({"_id": id})

        if user is None:
            raise UserNotFoundError("User not found.")

        user["id"] = user["_id"]
        return User.parse_obj(user)
