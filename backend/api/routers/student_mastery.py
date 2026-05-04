from fastapi import APIRouter, Depends
from typing import List
from api.schemas import StudentMasteryRes, StudentMasteryBase, StudentSkillMetricRes, StudentSkillMetricBase
from services import mastery_service
from core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/", response_model=StudentMasteryRes)
def update_mastery(progress_data: StudentMasteryBase):
    response = mastery_service.update_student_mastery(progress_data.model_dump())
    return response.data[0]

@router.get("/student/{student_id}", response_model=List[StudentMasteryRes])
def get_student_mastery(student_id: str):
    response = mastery_service.get_student_mastery(student_id)
    return response.data

@router.get("/skills/{student_id}", response_model=List[StudentSkillMetricRes])
def get_student_skills(student_id: str):
    response = mastery_service.get_skill_metrics(student_id)
    return response.data
