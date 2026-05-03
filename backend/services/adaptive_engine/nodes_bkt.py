# services/adaptive_engine/nodes_bkt.py
from services.adaptive_engine.graph_state import AdaptiveGraphState

def evaluate_performance(state: AdaptiveGraphState) -> dict:
    """Scores recent performance and updates BKT probabilistic models."""
    
    is_correct = str(state["student_answer"]).strip().lower() == str(state["correct_answer"]).strip().lower()
    
    # Bayesian Knowledge Tracing (BKT) Parameters
    P_L = state.get("ability_level", 0.5)  # Prior Probability of Learning
    P_G = 0.2  # Probability of Guessing correctly even if not learned
    P_S = 0.1  # Probability of Slipping (getting it wrong despite knowing it)
    P_T = 0.1  # Transition probability (learning from the question itself)
    
    # Update Probability based on Observation (Bayes Theorem)
    if is_correct:
        numerator = P_L * (1 - P_S)
        denominator = numerator + (1 - P_L) * P_G
    else:
        numerator = P_L * P_S
        denominator = numerator + (1 - P_L) * (1 - P_G)
        
    # Posterior probability given observation
    if denominator == 0:
        P_L_given_obs = P_L
    else:
        P_L_given_obs = numerator / denominator
        
    # Add transition probability (probability they learned it by doing the step)
    new_ability = P_L_given_obs + (1 - P_L_given_obs) * P_T
    
    # Simple confidence metric
    current_confidence = state.get("confidence_score", 0.5)
    if is_correct:
        new_confidence = min(1.0, current_confidence + 0.1)
    else:
        new_confidence = max(0.0, current_confidence - 0.1)
        
    return {
        "is_correct": is_correct,
        "ability_level": round(new_ability, 3),
        "confidence_score": round(new_confidence, 3)
    }