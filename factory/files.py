from typing import IO
from bson import ObjectId
from gridfs import GridOut, NoFile
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from models.schemas import FileInfo
from settings import settings


class Files:
    def __init__(self, database: str = 'ppfs', bucket_name: str = 'files'):
        client = AsyncIOMotorClient(
            host=settings.mongodb_host,
            username=settings.mongodb_username,
            password=settings.mongodb_password
        )
        self.__bucket = AsyncIOMotorGridFSBucket(client[database], bucket_name=bucket_name)

    async def list(self) -> list[FileInfo]:
        cursor = self.__bucket.find()
        return [
            FileInfo(id=ObjectId(file._id), filename=file.filename, content_type=file.metadata['type'])
            async for file in cursor
        ]

    async def get(self, id: ObjectId) -> FileInfo:
        cursor = self.__bucket.find({'_id': id}, limit=1)

        # Note: to_list returns documents, not GridOut!
        files: list[dict] = await cursor.to_list(length=1)
        if len(files) == 0:
            raise NoFile("File with given ID is not found.")

        file = files[0]
        return FileInfo(id=file['_id'], filename=file['filename'], content_type=file['metadata']['type'])

    async def upload_file(self, filename: str, file: IO, content_type: str, id: ObjectId | None = None) -> FileInfo:
        if id is None:
            file_id = await self.__bucket.upload_from_stream(
                filename, file, metadata={'type': content_type}
            )
        else:
            await self.__bucket.upload_from_stream_with_id(
                id, filename, file, metadata={'type': content_type}
            )
            file_id = id
        return FileInfo(id=file_id, filename=filename, content_type=content_type)

    async def delete(self, id: ObjectId) -> None:
        await self.__bucket.delete(id)

    async def rename(self, id: ObjectId, name: str) -> None:
        await self.__bucket.rename(id, name)

    async def get_download_stream(self, id: ObjectId | None = None, name: str | None = None) -> GridOut:
        if isinstance(id, ObjectId):
            return await self.__bucket.open_download_stream(id)
        if isinstance(name, str):
            return await self.__bucket.open_download_stream_by_name(name)
        raise TypeError("Either file id or name expected")
