from fastapi import HTTPException
from core.database import supabase

def create_user(user_data: dict):
    user_data["email"] = user_data.get("email", "").lower().strip() 
    if not user_data["email"]:
        raise HTTPException(status_code=400, detail="Email is required")
    
    return supabase.table("User").insert(user_data).execute() 

def get_user_by_email(email: str):
    response = supabase.table("User").select("*").eq("email", email).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]

def update_user_password(user_id: str, new_password: str):
    if not new_password:
        raise HTTPException(status_code=400, detail="New password cannot be empty")
    
    update_data = {
        "password": new_password,
        "updated_at": "now()" 
    }
    
    return supabase.table("User").update(update_data).eq("user_id", user_id).execute()

def update_user_details(user_id: str, update_data: dict):
    if "email" in update_data:
        raise HTTPException(status_code=400, detail="Email cannot be updated through this endpoint")
    
    update_data["updated_at"] = "now()" 
    
    return supabase.table("User").update(update_data).eq("user_id", user_id).execute()

def delete_user(user_id: str):
    return supabase.table("User").delete().eq("user_id", user_id).execute()
