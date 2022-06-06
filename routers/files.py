from fastapi import APIRouter, Depends, UploadFile

from dependencies import get_current_user, get_privileged_user
from models.dataclasses import User

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
    return {"e": [1, 2, 3]}


@read_router.get("/{id}")
async def get_by_id(id: str):
    return {"id": id}


# Privileged users: add, edit and delete files
@write_router.post("/new")
async def create_new_file():
    return {"info": "some id"}


@write_router.put("/{id}")
async def upload_file(id: str, file: UploadFile):
    return {"info": {"name": file.filename, "id": id}}


@write_router.delete("/{id}")
async def delete_file(id: str):
    return {"info": {"id": id}}
