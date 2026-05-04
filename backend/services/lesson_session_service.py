from fastapi import HTTPException
from core.database import supabase

def start_lesson_session(session_data: dict):
    return supabase.table("lesson_sessions").insert(session_data).execute()

def get_session_by_id(session_id: str):
    response = supabase.table("lesson_sessions").select("*").eq("id", session_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Session not found")
    return response.data[0]

def update_session_state(session_id: str, state: str, score: int = None):
    update_data = {
        "state": state
    }
    if score is not None:
        update_data["score"] = score
        
    return supabase.table("lesson_sessions").update(update_data).eq("id", session_id).execute()
