from fastapi import HTTPException
from core.database import supabase

def get_questions_by_skill(skill_id: str):
    response = supabase.table("questions").select("*").eq("skill_id", skill_id).execute() 
    if not response.data:
        raise HTTPException(status_code=404, detail=f"No questions found for skill {skill_id}")
    return response.data

def add_new_question(question_data: dict):
    if not question_data.get("content_payload"):
        raise HTTPException(status_code=400, detail="content_payload cannot be empty")
            
    return supabase.table("questions").insert(question_data).execute()

def update_question(question_id: str, update_data: dict):
    return supabase.table("questions").update(update_data).eq("id", question_id).execute()

def delete_question(question_id: str):
    return supabase.table("questions").delete().eq("id", question_id).execute()
