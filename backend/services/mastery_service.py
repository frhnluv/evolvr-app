from fastapi import HTTPException
from core.database import supabase

def update_student_mastery(mastery_data: dict):
    # Upserts the standard-level mastery
    return supabase.table("student_mastery").upsert(mastery_data, on_conflict="student_id, standard_id").execute()

def get_student_mastery(student_id: str):
    return supabase.table("student_mastery").select("*").eq("student_id", student_id).execute()

def update_skill_metrics(metrics_data: dict):
    # Upserts granular skill-level BKT/IRT metrics
    return supabase.table("student_skill_metrics").upsert(metrics_data, on_conflict="student_id, skill_id").execute()

def get_skill_metrics(student_id: str):
    return supabase.table("student_skill_metrics").select("*").eq("student_id", student_id).execute()
