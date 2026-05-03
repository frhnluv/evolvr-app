# services/adaptive_engine/graph.py
from langgraph.graph import StateGraph, END
from services.adaptive_engine.graph_state import AdaptiveGraphState
from services.adaptive_engine.nodes_bkt import evaluate_performance
from services.adaptive_engine.hint_generator import generate_scaffolded_hint
from services.adaptive_engine.nodes_irt import select_next_question

def route_evaluation(state: AdaptiveGraphState) -> str:
    """Routing logic based on correctness and max attempts."""
    if state["is_correct"]:
        return "select_next"
    elif state["attempt_number"] < 3: # Allow up to 2 hints before moving on
        return "generate_hint"
    else:
        # Failed 3 times. We move to the next (likely easier) question
        return "select_next"

# 1. Initialize the Graph
workflow = StateGraph(AdaptiveGraphState)

# 2. Add Nodes
workflow.add_node("evaluate", evaluate_performance)
workflow.add_node("generate_hint", generate_scaffolded_hint)
workflow.add_node("select_next", select_next_question)

# 3. Define the Edges (The Flow)
workflow.set_entry_point("evaluate")

workflow.add_conditional_edges(
    "evaluate",
    route_evaluation,
    {
        "select_next": "select_next",
        "generate_hint": "generate_hint"
    }
)

workflow.add_edge("generate_hint", END)
workflow.add_edge("select_next", END)

# 4. Compile the Engine
adaptive_engine = workflow.compile()