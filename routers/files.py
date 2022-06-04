from fastapi import APIRouter, Depends, UploadFile
from dependencies import get_current_user

router = APIRouter()


@router.get("/")
async def get_list():
    return {"e": [1, 2, 3]}


@router.post("/new")
async def create_new(user: str = Depends(get_current_user)):
    return {"info": "some id", "user": user}


@router.get("/{id}")
async def get_by_id(id: int):
    return {"id": id}


@router.put("/{id}")
async def upload(id: int, file: UploadFile, user: str = Depends(get_current_user)):
    return {"info": {"name": file.filename}, "user": user}


@router.delete("/{id}")
async def delete(id: int, file: UploadFile, user: str = Depends(get_current_user)):
    return {"info": {"name": file.filename}, "user": user}
