import asyncio
from bson import ObjectId
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

from models.dataclasses import User
from exceptions.auth import InvalidCredentialsError, UserNotFoundError
from models.schemas import UserAuthentication
from settings import settings


class Users:
    def __init__(self, database: str = 'ppfs', collection: str = 'users'):
        client = AsyncIOMotorClient(
            host=settings.mongodb_host,
            username=settings.mongodb_username,
            password=settings.mongodb_password
        )
        self.__collection = client[database][collection]
        self.__password_context = CryptContext(schemes=["bcrypt"])

        asyncio.run_coroutine_threadsafe(
            self.__create_index(),
            loop=asyncio.get_running_loop()
        )

    async def __create_index(self):
        await self.__collection.create_index('username', unique=True)

    async def authenticate(self, user_auth: UserAuthentication) -> User:
        user = await self.__collection.find_one({'username': user_auth.username})
        user['id'] = user['_id']

        if user is None or not self.__password_context.verify(user_auth.password, user['password']):
            raise InvalidCredentialsError("Invalid username or password.")

        return User.parse_obj(user)

    async def create(self, user_auth: UserAuthentication, is_admin: bool) -> User:
        try:
            result = await self.__collection.insert_one({
                'username': user_auth.username,
                'password': self.__password_context.hash(user_auth.password),
                'is_admin': is_admin
            })
        except DuplicateKeyError:
            raise InvalidCredentialsError("Username is already taken.")
        return User(id=result.inserted_id, username=user_auth.username, is_admin=is_admin)

    async def get(self, id: ObjectId) -> User:
        user = await self.__collection.find_one({'_id': id})
        user['id'] = user['_id']

        if user is None:
            raise UserNotFoundError("User not found.")

        return User.parse_obj(user)
