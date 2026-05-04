from fastapi import HTTPException
from core.database import supabase

def record_response(response_data: dict):
    return supabase.table("responses").insert(response_data).execute()

def get_responses_by_session(session_id: str):
    return supabase.table("responses").select("*").eq("lesson_session_id", session_id).execute()

def get_responses_by_student(student_id: str):
    # Need to join with lesson_sessions to filter by student
    return supabase.table("responses").select("*, lesson_sessions!inner(student_id)").eq("lesson_sessions.student_id", student_id).execute()
