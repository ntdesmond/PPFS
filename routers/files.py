from fastapi import APIRouter, Depends, UploadFile

from dependencies import get_current_user
from models.dataclasses import User

router = APIRouter(tags=["Files"])


@router.get("/")
async def get_list():
    return {"e": [1, 2, 3]}


@router.post("/new")
async def create_new(user: User = Depends(get_current_user)):
    return {"info": "some id", "user": str(user.id)}


@router.get("/{id}")
async def get_by_id(id: str):
    return {"id": id}


@router.put("/{id}")
async def upload(id: str, file: UploadFile, user: User = Depends(get_current_user)):
    return {"info": {"name": file.filename}, "user": user}


@router.delete("/{id}")
async def delete(id: str, file: UploadFile, user: User = Depends(get_current_user)):
    return {"info": {"name": file.filename}, "user": user}
