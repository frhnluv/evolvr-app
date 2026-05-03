# test_engine.py
from services.adaptive_engine.graph import adaptive_engine


def print_result(scenario_name, final_state):
    print(f"\n{'=' * 40}")
    print(f" {scenario_name} ")
    print(f"{'=' * 40}")
    print(f"User Answer:      {final_state.get('student_answer')}")
    print(f"Is Correct:       {final_state.get('is_correct')}")
    print(f"Ability Level:    {final_state.get('ability_level')} (IRT Theta)")
    print(f"Confidence Score: {final_state.get('confidence_score')} (BKT Prob)")
    print(f"Next Attempt #:   {final_state.get('attempt_number')}")

    if final_state.get('hint_payload'):
        print(f"\n[GEMINI HINT GENERATED]")
        print(f"Level {final_state['hint_payload']['hint_level']}: {final_state['hint_payload']['content']}")

    if final_state.get('next_question_id'):
        print(f"\n[MOVING TO NEXT QUESTION]")
        print(f"Target ID: {final_state['next_question_id']}")
    print(f"{'=' * 40}\n")


def run_tests():
    # The starting baseline for our simulated student
    base_state = {
        "student_id": "test-student-123",
        "skill_id": "skill-addition-01",
        "question_id": "q-001",
        "correct_answer": "4",
        "ability_level": 0.5,  # Baseline ability
        "confidence_score": 0.5,  # Baseline confidence
        "attempt_number": 1,
        "hint_payload": None,
        "next_question_id": None
    }

    # ---------------------------------------------------------
    # SCENARIO 1: Student gets the answer right on the first try
    # ---------------------------------------------------------
    state_1 = base_state.copy()
    state_1["student_answer"] = "4"
    print("Executing Scenario 1...")
    result_1 = adaptive_engine.invoke(state_1)
    print_result("SCENARIO 1: CORRECT ANSWER", result_1)

    # ---------------------------------------------------------
    # SCENARIO 2: Student gets the answer wrong (Attempt 1)
    # Expected: Triggers Gemini to generate a gentle hint
    # ---------------------------------------------------------
    state_2 = base_state.copy()
    state_2["student_answer"] = "5"
    print("Executing Scenario 2 (Calling Gemini API)...")
    result_2 = adaptive_engine.invoke(state_2)
    print_result("SCENARIO 2: INCORRECT (ATTEMPT 1)", result_2)

    # ---------------------------------------------------------
    # SCENARIO 3: Student gets it wrong repeatedly (Attempt 3)
    # Expected: Bypasses hint generation, moves to next question
    # ---------------------------------------------------------
    state_3 = base_state.copy()
    state_3["student_answer"] = "6"
    state_3["attempt_number"] = 3
    print("Executing Scenario 3...")
    result_3 = adaptive_engine.invoke(state_3)
    print_result("SCENARIO 3: INCORRECT (MAX ATTEMPTS)", result_3)


if __name__ == "__main__":
    run_tests()