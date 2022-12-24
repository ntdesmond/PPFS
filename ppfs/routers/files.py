from bson import ObjectId
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import StreamingResponse, Response

from ..dependencies import get_current_user, get_privileged_user, get_id
from ..factory import get_file_factory, Files
from ..models.schemas import FileInfo
from ..utils.files import get_file_chunks

read_router = APIRouter(tags=["Read files"], dependencies=[Depends(get_current_user)])
write_router = APIRouter(
    tags=["Write files"], dependencies=[Depends(get_privileged_user)]
)


# Unprivileged users: list and get files
@read_router.get("/", status_code=status.HTTP_200_OK, response_model=list[FileInfo])
async def get_files_list(files: Files = Depends(get_file_factory)):
    return await files.list()


@read_router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_class=StreamingResponse
)
async def get_file_content(
    id: ObjectId = Depends(get_id), files: Files = Depends(get_file_factory)
):
    file_info = await files.get(id)
    file_content = get_file_chunks(await files.get_download_stream(id=id))
    return StreamingResponse(file_content, media_type=file_info.content_type)


# Privileged users: add, edit and delete files
@write_router.post("/new", status_code=status.HTTP_201_CREATED, response_model=FileInfo)
async def create_new_file(file: UploadFile, files: Files = Depends(get_file_factory)):
    return await files.upload_file(file.filename, file.file, file.content_type)


@write_router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=FileInfo)
async def rename_file(
    new_name: str,
    id: ObjectId = Depends(get_id),
    files: Files = Depends(get_file_factory),
):
    await files.rename(id, new_name)
    return await files.get(id)


@write_router.delete(
    "/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
async def delete_file(
    id: ObjectId = Depends(get_id), files: Files = Depends(get_file_factory)
):
    await files.delete(id)
