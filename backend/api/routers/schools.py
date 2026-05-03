from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.schemas import SchoolCreate, SchoolRes
from services import school_service
from core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/", response_model=SchoolRes, status_code=201)
def create_school(school: SchoolCreate):
    result = school_service.create_school(school.model_dump())
    if not result.data:
        raise HTTPException(status_code=400, detail="Creation failed")
    return result.data[0]

@router.get("/{school_id}", response_model=SchoolRes)
def get_school(school_id: str):
    return school_service.get_school_by_id(school_id)

@router.put("/{school_id}")
def update_school(school_id: str, school_name: str):
    result = school_service.update_school_name(school_id, school_name)
    if not result.data:
        raise HTTPException(status_code=400, detail="Update failed")
    return result.data[0]

@router.delete("/{school_id}", status_code=204)
def delete_school(school_id: str):
    school_service.delete_school(school_id)
    return None
