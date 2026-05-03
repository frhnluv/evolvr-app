# services/adaptive_engine/nodes_irt.py
from services.adaptive_engine.graph_state import AdaptiveGraphState

def select_next_question(state: AdaptiveGraphState) -> dict:
    """Selects the next question based on Item Response Theory difficulty matching ."""
    
    # In reality, this queries your Supabase `questions` table:
    # SELECT id FROM questions WHERE skill_id = state['skill_id'] 
    # ORDER BY ABS(difficulty_parameter - state['ability_level']) ASC LIMIT 1
    
    simulated_next_question_id = "uuid-of-next-best-question"
    
    return {
        "next_question_id": simulated_next_question_id,
        "hint_payload": None, # Clear any previous hints
        "attempt_number": 1   # Reset attempts for the new question
    }