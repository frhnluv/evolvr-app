from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from api.schemas import StudentMasteryDashboard, ClassReportResponse
from services import report_service
from core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/student/{student_id}", response_model=StudentMasteryDashboard)
def get_student_mastery(student_id: str):
    return report_service.get_student_mastery_dashboard(student_id)

@router.get("/class/{class_id}/teacher/{teacher_id}", response_model=ClassReportResponse)
def get_class_report(teacher_id: str, class_id: str):
    return report_service.get_class_report(teacher_id, class_id)

@router.get("/session/{session_id}/analytics")
def get_session_analytics(session_id: str):
    return report_service.get_session_analytics(session_id)
