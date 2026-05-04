from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.schemas import HintCreate, HintRes
from services import hint_service
from core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/question/{question_id}", response_model=List[HintRes])
def get_hints(question_id: str):
    result = hint_service.get_hints_for_question(question_id)
    return result.data
