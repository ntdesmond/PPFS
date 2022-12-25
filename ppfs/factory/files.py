from typing import IO
from bson import ObjectId
from gridfs import GridOut, NoFile
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from ..models.schemas import FileDescription, FileInfo, OptionalFileDescription
from ..settings import settings


class Files:
    def __init__(self, database: str = "ppfs", bucket_name: str = "files"):
        client = AsyncIOMotorClient(
            host=settings.mongodb.host,
            username=settings.mongodb.username,
            password=settings.mongodb.password,
        )
        self.__bucket = AsyncIOMotorGridFSBucket(
            client[database], bucket_name=bucket_name
        )
        self.__files_collection = client[database][f"{bucket_name}.files"]

    async def list(self) -> list[FileInfo]:
        cursor = self.__bucket.find()
        return [
            FileInfo(
                id=file._id,
                filename=file.filename,
                content_type=file.metadata["type"],
                description=file.metadata["description"],
            )
            async for file in cursor
        ]

    async def get(self, id: ObjectId) -> FileInfo:
        cursor = self.__bucket.find({"_id": id}, limit=1)

        # Note: to_list returns documents, not GridOut!
        files: list[dict] = await cursor.to_list(length=1)
        if len(files) == 0:
            raise NoFile("File with given ID is not found.")

        file = files[0]
        return FileInfo(
            id=file["_id"],
            filename=file["filename"],
            content_type=file["metadata"]["type"],
            description=file["metadata"]["description"],
        )

    async def upload_file(
        self,
        filename: str,
        file: IO,
        content_type: str,
        description: FileDescription,
        id: ObjectId | None = None,
    ) -> FileInfo:
        metadata = {
            "type": content_type,
            "description": description.dict(),
        }
        if id is None:
            file_id = await self.__bucket.upload_from_stream(
                filename, file, metadata=metadata
            )
        else:
            await self.__bucket.upload_from_stream_with_id(
                id, filename, file, metadata=metadata
            )
            file_id = id
        return FileInfo(
            id=str(file_id),
            filename=filename,
            content_type=content_type,
            description=description,
        )

    async def delete(self, id: ObjectId) -> None:
        await self.__bucket.delete(id)

    async def rename(self, id: ObjectId, name: str) -> None:
        try:
            await self.__bucket.rename(id, name)
        except TypeError:  # workaround on a format bug (%i)
            pass

    async def update_description(
        self, id: ObjectId, description: OptionalFileDescription
    ) -> None:
        await self.__files_collection.update_one(
            {"_id": id},
            {
                "$set": {
                    f"metadata.description.{key}": value
                    for key, value in description.dict(exclude_unset=True).items()
                }
            },
        )

    async def get_download_stream(
        self, id: ObjectId | None = None, name: str | None = None
    ) -> GridOut:
        if isinstance(id, ObjectId):
            return await self.__bucket.open_download_stream(id)
        if isinstance(name, str):
            return await self.__bucket.open_download_stream_by_name(name)
        raise TypeError("Either file id or name expected")
