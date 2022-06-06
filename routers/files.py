from fastapi import APIRouter, Depends, UploadFile

from dependencies import get_current_user, get_privileged_user
from models.dataclasses import User

router = APIRouter(tags=["Files"])


# Unprivileged users: list and get files
@router.get("/")
async def get_list(user: User = Depends(get_current_user)):
    return {"e": [1, 2, 3], "user": user}


@router.get("/{id}")
async def get_by_id(id: str, user: User = Depends(get_current_user)):
    return {"id": id, "user": user}


# Privileged users: add, edit and delete files
@router.post("/new")
async def create_new(user: User = Depends(get_privileged_user)):
    return {"info": "some id", "user": user}


@router.put("/{id}")
async def upload(id: str, file: UploadFile, user: User = Depends(get_privileged_user)):
    return {"info": {"name": file.filename}, "user": user}


@router.delete("/{id}")
async def delete(id: str, file: UploadFile, user: User = Depends(get_privileged_user)):
    return {"info": {"name": file.filename}, "user": user}
