from fastapi import HTTPException
from core.database import supabase

def create_student(student_data: dict):
    return supabase.table("students").insert(student_data).execute()

def get_student_by_id(student_id: str):
    response = supabase.table("students").select("*, users(name, email)").eq("id", student_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Student not found")
    return response.data[0]

def get_all_students():
    return supabase.table("students").select("*, users(name, email)").execute()

def update_student_details(student_id: str, update_data: dict):
    return supabase.table("students").update(update_data).eq("id", student_id).execute()

def delete_student(student_id: str):
    return supabase.table("students").delete().eq("id", student_id).execute()
