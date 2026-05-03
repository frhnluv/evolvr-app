# services/adaptive_engine/nodes_irt.py
from services.adaptive_engine.graph_state import AdaptiveGraphState
from core.database import supabase

def select_next_question(state: AdaptiveGraphState) -> dict:
    """Selects the next question based on Item Response Theory difficulty matching."""
    
    # Fetch questions for the given skill (using 'strand' as skill_id for now)
    skill_id = state.get('skill_id')
    response = supabase.table("questions").select("id, difficulty_parameter").eq("strand", skill_id).execute()
    
    next_question_id = None
    if response.data:
        ability = state.get('ability_level', 0.5)
        # Find the question with difficulty_parameter closest to student's ability_level
        sorted_questions = sorted(
            response.data, 
            key=lambda q: abs(q.get("difficulty_parameter", 0.5) - ability)
        )
        if sorted_questions:
            next_question_id = sorted_questions[0]["id"]
            
    return {
        "next_question_id": next_question_id,
        "hint_payload": None, # Clear any previous hints
        "attempt_number": 1   # Reset attempts for the new question
    }