from fastapi import HTTPException
from core.database import supabase

def create_school(school_data: dict):
    return supabase.table("School").insert(school_data).execute()

def get_school_by_id(school_id: str):
    response = supabase.table("School").select("*").eq("school_id", school_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="School not found")
    return response.data[0]

def update_school_name(school_id: str, school_name: str):
    update_data = {
        "school_name": school_name
    }
    return supabase.table("School").update(update_data).eq("school_id", school_id).execute()

def delete_school(school_id: str):
    return supabase.table("School").delete().eq("school_id", school_id).execute()
