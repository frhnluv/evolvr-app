from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.schemas import UserCreate, UserRes
from services import user_service
from core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=UserRes, status_code=201)
def create_user(user: UserCreate):
    result = user_service.create_user(user.model_dump())
    if not result.data:
        raise HTTPException(status_code=400, detail="Registration failed")
    return result.data[0]

@router.get("/{email}", response_model=UserRes, dependencies=[Depends(get_current_user)])
def get_user(email: str):
    return user_service.get_user_by_email(email)



@router.delete("/{user_id}", status_code=204, dependencies=[Depends(get_current_user)])
def delete_user(user_id: str):
    user_service.delete_user(user_id)
    return None
