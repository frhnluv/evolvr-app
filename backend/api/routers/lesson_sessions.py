from fastapi import APIRouter, Depends
from api.schemas import LessonSessionRes, LessonSessionCreate
from services import lesson_session_service
from core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/", response_model=LessonSessionRes)
def start_session(session_data: LessonSessionCreate):
    response = lesson_session_service.start_lesson_session(session_data.model_dump())
    return response.data[0]

@router.get("/{session_id}", response_model=LessonSessionRes)
def get_session(session_id: str):
    return lesson_session_service.get_session_by_id(session_id)

@router.put("/{session_id}/state")
def update_session_state(session_id: str, state: str, score: int = None):
    response = lesson_session_service.update_session_state(session_id, state, score)
    return response.data[0]
