from fastapi import APIRouter, Depends
from typing import List
from api.schemas import ResponseRes, ResponseCreate
from services import response_service
from core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/", response_model=ResponseRes)
def submit_response(response_data: ResponseCreate):
    response = response_service.record_response(response_data.model_dump())
    return response.data[0]

@router.get("/session/{session_id}", response_model=List[ResponseRes])
def get_responses_for_session(session_id: str):
    response = response_service.get_responses_by_session(session_id)
    return response.data

@router.get("/student/{student_id}", response_model=List[ResponseRes])
def get_responses_for_student(student_id: str):
    response = response_service.get_responses_by_student(student_id)
    return response.data
