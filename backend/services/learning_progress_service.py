from core.database import supabase

def upsert_learning_progress(progress_data: dict):
    return supabase.table("LearningProgress").upsert(progress_data).execute()

def get_learning_progress(student_id: str):
    return supabase.table("LearningProgress").select("*").eq("student_id", student_id).execute()
