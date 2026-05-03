# services/adaptive_engine/graph_state.py
from typing import TypedDict, Optional, Dict, Any

class AdaptiveGraphState(TypedDict):
    student_id: str
    skill_id: str
    question_id: str
    student_answer: str
    correct_answer: str
    attempt_number: int
    
    # Adaptive metrics
    is_correct: Optional[bool]
    ability_level: float       # The IRT Theta parameter
    confidence_score: float    # The BKT mastery probability
    
    # Engine Outputs
    hint_payload: Optional[Dict[str, Any]]
    next_question_id: Optional[str]