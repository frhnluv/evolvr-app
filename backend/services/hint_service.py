from core.database import supabase

def get_hints_by_question(question_id: str):
    return supabase.table("Hint").select("*").eq("question_id", question_id).execute()

def create_hint_usage(usage_data: dict):
    return supabase.table("HintUsage").insert(usage_data).execute()
