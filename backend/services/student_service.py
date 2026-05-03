from fastapi import HTTPException
from core.database import supabase

def create_student(student_data: dict):
    return supabase.table("students").insert(student_data).execute()

def get_student_by_id(student_id: str):
    response = supabase.table("students").select("*").eq("id", student_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Student not found")
    return response.data[0]

def get_all_students():
    return supabase.table("students").select("*").execute()

def update_student_progress(student_id: str, score: float):
    if not (0 <= score <= 100):
        raise HTTPException(status_code=400, detail="Performance score must be between 0 and 100")
    
    status = "Exceeding Expectations" if score >= 80 else "Developing"
    
    update_data = {
        "performance": score,
        "status": status,
        "updated_at": "now()" 
    }
    
    return supabase.table("students").update(update_data).eq("id", student_id).execute()

def update_student_details(student_id: str, update_data: dict):
    if "performance" in update_data or "status" in update_data:
        raise HTTPException(status_code=400, detail="Performance and status cannot be updated through this endpoint")
    
    update_data["updated_at"] = "now()" 
    
    return supabase.table("students").update(update_data).eq("id", student_id).execute()

def delete_student(student_id: str):
    return supabase.table("students").delete().eq("id", student_id).execute()
