from fastapi import HTTPException
from core.database import supabase

def create_teacher(teacher_data: dict):
    return supabase.table("teachers").insert(teacher_data).execute()

def get_teacher_by_id(teacher_id: str):
    response = supabase.table("teachers").select("*, users(name, email)").eq("id", teacher_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return response.data[0]

def get_teacher_dashboard(teacher_id: str):
    # Fetch classes for teacher, then enrollments, then students
    classes_res = supabase.table("classes").select("id, name, class_enrollments(students(id, users(name)))").eq("teacher_id", teacher_id).execute()
    return classes_res.data

def update_teacher_details(teacher_id: str, update_data: dict):
    return supabase.table("teachers").update(update_data).eq("id", teacher_id).execute()

def delete_teacher(teacher_id: str):
    return supabase.table("teachers").delete().eq("id", teacher_id).execute()
