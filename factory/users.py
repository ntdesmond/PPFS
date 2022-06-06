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

        if user is None or not self.__password_context.verify(user_auth.password, user['password']):
            raise InvalidCredentialsError("Invalid username or password.")

        return User(id=user['_id'], username=user['username'])

    async def create(self, user_auth: UserAuthentication) -> User:
        try:
            result = await self.__collection.insert_one({
                'username': user_auth.username,
                'password': self.__password_context.hash(user_auth.password)
            })
        except DuplicateKeyError:
            raise InvalidCredentialsError("Username is already taken.")
        return User(id=result.inserted_id, username=user_auth.username)

    async def get(self, id: ObjectId) -> User:
        user = await self.__collection.find_one({'_id': id})

        if user is None:
            raise UserNotFoundError("User not found.")

        return User(id=user['_id'], username=user['username'])
