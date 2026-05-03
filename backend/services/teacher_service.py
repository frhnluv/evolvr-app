from fastapi import HTTPException
from core.database import supabase

def create_teacher(teacher_data: dict):
    return supabase.table("teachers").insert(teacher_data).execute()

def get_teacher_by_id(teacher_id: str):
    response = supabase.table("teachers").select("*").eq("id", teacher_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return response.data[0]

def get_teacher_dashboard(teacher_id: str):
    return supabase.table("students").select("id, performance, status").eq("teacher_id", teacher_id).execute()

def update_teacher_details(teacher_id: str, update_data: dict):
    update_data["updated_at"] = "now()" 
    
    return supabase.table("teachers").update(update_data).eq("id", teacher_id).execute()

def delete_teacher(teacher_id: str):
    return supabase.table("teachers").delete().eq("id", teacher_id).execute()
