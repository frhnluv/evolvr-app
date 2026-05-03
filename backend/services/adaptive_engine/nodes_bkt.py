# services/adaptive_engine/nodes_bkt.py
from services.adaptive_engine.graph_state import AdaptiveGraphState

def evaluate_performance(state: AdaptiveGraphState) -> dict:
    """Scores recent performance and updates BKT probabilistic models [cite: 625-627, 630]."""
    
    is_correct = str(state["student_answer"]).strip().lower() == str(state["correct_answer"]).strip().lower()
    
    # Simplified BKT / IRT mathematical update
    # In a production environment, this would use the standard BKT formula: P(L|Obs)
    current_ability = state["ability_level"]
    current_confidence = state["confidence_score"]
    
    if is_correct:
        # Increase ability and confidence
        new_ability = current_ability + 0.15
        new_confidence = min(1.0, current_confidence + 0.2)
    else:
        # Decrease ability and confidence (penalty is lower to prevent discouragement)
        new_ability = current_ability - 0.05
        new_confidence = max(0.0, current_confidence - 0.1)
        
    return {
        "is_correct": is_correct,
        "ability_level": round(new_ability, 3),
        "confidence_score": round(new_confidence, 3)
    }