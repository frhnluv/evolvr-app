from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.schemas import StudentCreate, StudentRes
from services import student_service
from core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/", response_model=StudentRes, status_code=201)
def create_student(student: StudentCreate):
    result = student_service.create_student(student.model_dump())
    if not result.data:
        raise HTTPException(status_code=400, detail="Registration failed")
    return result.data[0]

@router.get("/{student_id}", response_model=StudentRes)
def get_student(student_id: str):
    return student_service.get_student_by_id(student_id)

@router.get("/", response_model=List[StudentRes])
def get_all_students():
    result = student_service.get_all_students()
    return result.data



@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: str):
    student_service.delete_student(student_id)
    return None
