from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.schemas import LearningSessionCreate, LearningSessionRes
from services import learning_session_service
from core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/", response_model=LearningSessionRes, status_code=201)
def create_session(session: LearningSessionCreate):
    result = learning_session_service.create_learning_session(session.model_dump())
    if not result.data:
        raise HTTPException(status_code=400, detail="Creation failed")
    return result.data[0]

@router.get("/{session_id}", response_model=LearningSessionRes)
def get_session(session_id: str):
    return learning_session_service.get_session_by_id(session_id)

@router.put("/{session_id}/end")
def end_session(session_id: str):
    result = learning_session_service.end_learning_session(session_id)
    if not result.data:
        raise HTTPException(status_code=400, detail="Update failed")
    return result.data[0]
