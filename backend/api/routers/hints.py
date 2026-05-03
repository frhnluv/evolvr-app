from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.schemas import HintCreate, HintResponse, HintUsageCreate, HintUsageResponse
from services import hint_service
from core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/question/{question_id}", response_model=List[HintResponse])
def get_hints(question_id: str):
    result = hint_service.get_hints_by_question(question_id)
    return result.data

@router.post("/usage", response_model=HintUsageResponse, status_code=201)
def log_hint_usage(usage: HintUsageCreate):
    result = hint_service.create_hint_usage(usage.model_dump())
    if not result.data:
        raise HTTPException(status_code=400, detail="Creation failed")
    return result.data[0]
