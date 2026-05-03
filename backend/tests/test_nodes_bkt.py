import pytest
from services.adaptive_engine.nodes_bkt import evaluate_performance

def test_evaluate_performance_correct_answer():
    # Setup state where the student answers correctly
    state = {
        "student_answer": "4",
        "correct_answer": "4",
        "ability_level": 0.5,
        "confidence_score": 0.5
    }
    
    result = evaluate_performance(state)
    
    assert result["is_correct"] is True
    # Initial P_L=0.5, P_S=0.1, P_G=0.2
    # numerator = 0.5 * 0.9 = 0.45
    # denominator = 0.45 + (0.5 * 0.2) = 0.55
    # P_L_given_obs = 0.45 / 0.55 = 0.818
    # new_ability = 0.818 + (1 - 0.818) * 0.1 = 0.818 + 0.0182 = 0.836
    assert result["ability_level"] == 0.836
    # Confidence should increase by 0.1
    assert result["confidence_score"] == 0.6


def test_evaluate_performance_incorrect_answer():
    # Setup state where the student answers incorrectly
    state = {
        "student_answer": "3",
        "correct_answer": "4",
        "ability_level": 0.5,
        "confidence_score": 0.5
    }
    
    result = evaluate_performance(state)
    
    assert result["is_correct"] is False
    # Initial P_L=0.5, P_S=0.1, P_G=0.2
    # numerator = 0.5 * 0.1 = 0.05
    # denominator = 0.05 + (0.5 * 0.8) = 0.45
    # P_L_given_obs = 0.05 / 0.45 = 0.111
    # new_ability = 0.111 + (1 - 0.111) * 0.1 = 0.111 + 0.0889 = 0.2
    assert result["ability_level"] == 0.2
    # Confidence should decrease by 0.1
    assert result["confidence_score"] == 0.4
