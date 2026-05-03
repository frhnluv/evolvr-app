from core.database import supabase

def create_student_response(response_data: dict):
    return supabase.table("StudentResponse").insert(response_data).execute()

def get_responses_by_session(session_id: str):
    return supabase.table("StudentResponse").select("*").eq("session_id", session_id).execute()

def get_student_history(student_id: str):
    return supabase.table("StudentResponse").select("*").eq("student_id", student_id).execute()
