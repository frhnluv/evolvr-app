from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.schemas import StudentResponseCreate, StudentResponseRes
from services import student_response_service
from core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/", response_model=StudentResponseRes, status_code=201)
def create_response(response: StudentResponseCreate):
    result = student_response_service.create_student_response(response.model_dump())
    if not result.data:
        raise HTTPException(status_code=400, detail="Creation failed")
    return result.data[0]

@router.get("/session/{session_id}", response_model=List[StudentResponseRes])
def get_session_responses(session_id: str):
    result = student_response_service.get_responses_by_session(session_id)
    return result.data

@router.get("/student/{student_id}", response_model=List[StudentResponseRes])
def get_student_history(student_id: str):
    result = student_response_service.get_student_history(student_id)
    return result.data
