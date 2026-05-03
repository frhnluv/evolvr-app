from fastapi import HTTPException
from core.database import supabase

def get_questions_by_strand(strand_name: str):
    response = supabase.table("Question").select("*").eq("strand", strand_name).execute() 
    if not response.data:
        raise HTTPException(status_code=404, detail=f"No questions found for {strand_name}")
    return response.data

def add_new_question(question_data: dict):
    required_fields = ["question", "option_a", "option_b", "option_c", "option_d", "answer"]
    for field in required_fields:
        if not question_data.get(field):
            raise HTTPException(status_code=400, detail=f"Field '{field}' cannot be empty")
            
    return supabase.table("Question").insert(question_data).execute()

def update_question(question_id: str, update_data: dict):
    update_data["updated_at"] = "now()" 
    
    return supabase.table("Question").update(update_data).eq("question_id", question_id).execute()

def delete_question(question_id: str):
    return supabase.table("Question").delete().eq("question_id", question_id).execute()
