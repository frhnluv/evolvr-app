from core.database import supabase

def create_adaptive_decision(decision_data: dict):
    return supabase.table("AdaptiveDecision").insert(decision_data).execute()

def get_decisions_by_session(session_id: str):
    return supabase.table("AdaptiveDecision").select("*").eq("session_id", session_id).execute()
