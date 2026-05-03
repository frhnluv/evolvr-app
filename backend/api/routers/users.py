from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.schemas import UserCreate, UserRes
from services import user_service

router = APIRouter()

@router.post("/", response_model=UserRes, status_code=201)
def create_user(user: UserCreate):
    result = user_service.create_user(user.model_dump())
    if not result.data:
        raise HTTPException(status_code=400, detail="Registration failed")
    return result.data[0]

@router.get("/{email}", response_model=UserRes)
def get_user(email: str):
    return user_service.get_user_by_email(email)

@router.put("/{user_id}/password")
def update_password(user_id: str, new_password: str):
    result = user_service.update_user_password(user_id, new_password)
    return result.data

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str):
    user_service.delete_user(user_id)
    return None
