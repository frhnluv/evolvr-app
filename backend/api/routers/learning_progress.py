from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.schemas import LearningProgressCreate, LearningProgressResponse
from services import learning_progress_service
from core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/", response_model=LearningProgressResponse)
def upsert_progress(progress: LearningProgressCreate):
    result = learning_progress_service.upsert_learning_progress(progress.model_dump())
    if not result.data:
        raise HTTPException(status_code=400, detail="Upsert failed")
    return result.data[0]

@router.get("/student/{student_id}", response_model=List[LearningProgressResponse])
def get_student_progress(student_id: str):
    result = learning_progress_service.get_learning_progress(student_id)
    return result.data
