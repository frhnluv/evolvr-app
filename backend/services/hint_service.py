from fastapi import HTTPException
from core.database import supabase

def get_hints_for_question(question_id: str):
    return supabase.table("question_hints").select("*").eq("question_id", question_id).execute()

def create_hint(hint_data: dict):
    return supabase.table("question_hints").insert(hint_data).execute()

def record_hint_usage(response_id: str, hint_id: str):
    # hint usage is now tracked on the response table directly
    return supabase.table("responses").update({"hint_used_id": hint_id}).eq("id", response_id).execute()
