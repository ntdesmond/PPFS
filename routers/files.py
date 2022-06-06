from bson import ObjectId
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import StreamingResponse

from dependencies import get_current_user, get_privileged_user, get_id
from factory import files
from utils.files import get_file_chunks

read_router = APIRouter(
    tags=["Read files"],
    dependencies=[Depends(get_current_user)]
)
write_router = APIRouter(
    tags=["Write files"],
    dependencies=[Depends(get_privileged_user)]
)


# Unprivileged users: list and get files
@read_router.get("/")
async def get_files_list():
    return await files.list()


@read_router.get("/{id}")
async def get_file_content(id: ObjectId = Depends(get_id)):
    file_info = await files.get(id)
    file_content = get_file_chunks(await files.get_download_stream(id=id))
    return StreamingResponse(file_content, media_type=file_info.content_type)


# Privileged users: add, edit and delete files
@write_router.post("/new")
async def create_new_file(file: UploadFile):
    return await files.upload_file(file.filename, file.file, file.content_type)


@write_router.patch("/{id}")
async def rename_file(new_name: str, id: ObjectId = Depends(get_id)):
    await files.rename(id, new_name)
    return await files.get(id)


@write_router.delete("/{id}", status_code=204)
async def delete_file(id: ObjectId = Depends(get_id)):
    await files.delete(id)
