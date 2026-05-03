from fastapi import HTTPException
from core.database import supabase

def create_learning_session(session_data: dict):
    return supabase.table("LearningSession").insert(session_data).execute()

def get_session_by_id(session_id: str):
    response = supabase.table("LearningSession").select("*").eq("session_id", session_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Session not found")
    return response.data[0]

def end_learning_session(session_id: str):
    return supabase.table("LearningSession").update({
        "end_time": "now()"
    }).eq("session_id", session_id).execute()
