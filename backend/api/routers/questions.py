from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.schemas import QuestionCreate, QuestionRes
from services import question_service
from core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/", response_model=QuestionRes, status_code=201)
def create_question(question: QuestionCreate):
    result = question_service.add_new_question(question.model_dump())
    if not result.data:
        raise HTTPException(status_code=400, detail="Creation failed")
    return result.data[0]

@router.get("/strand/{strand_name}", response_model=List[QuestionRes])
def get_questions_by_strand(strand_name: str):
    return question_service.get_questions_by_strand(strand_name)

@router.delete("/{question_id}", status_code=204)
def delete_question(question_id: str):
    question_service.delete_question(question_id)
    return None
