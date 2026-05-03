from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.schemas import AdaptiveDecisionCreate, AdaptiveDecisionRes
from services import adaptive_decision_service
from core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/", response_model=AdaptiveDecisionRes, status_code=201)
def create_decision(decision: AdaptiveDecisionCreate):
    result = adaptive_decision_service.create_adaptive_decision(decision.model_dump())
    if not result.data:
        raise HTTPException(status_code=400, detail="Creation failed")
    return result.data[0]

@router.get("/session/{session_id}", response_model=List[AdaptiveDecisionRes])
def get_session_decisions(session_id: str):
    result = adaptive_decision_service.get_decisions_by_session(session_id)
    return result.data
