from fastapi import APIRouter, HTTPException
from typing import List
from api.schemas import TeacherCreate, TeacherRes, StudentRes
from services import teacher_service

router = APIRouter()

@router.post("/", response_model=TeacherRes, status_code=201)
def create_teacher(teacher: TeacherCreate):
    result = teacher_service.create_teacher(teacher.model_dump())
    if not result.data:
        raise HTTPException(status_code=400, detail="Registration failed")
    return result.data[0]

@router.get("/{teacher_id}", response_model=TeacherRes)
def get_teacher(teacher_id: str):
    return teacher_service.get_teacher_by_id(teacher_id)

@router.get("/{teacher_id}/dashboard", response_model=List[StudentRes])
def get_dashboard(teacher_id: str):
    result = teacher_service.get_teacher_dashboard(teacher_id)
    return result.data

@router.delete("/{teacher_id}", status_code=204)
def delete_teacher(teacher_id: str):
    teacher_service.delete_teacher(teacher_id)
    return None
