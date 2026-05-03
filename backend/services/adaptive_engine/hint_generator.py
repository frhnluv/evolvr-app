# services/adaptive_engine/hint_generator.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from services.adaptive_engine.graph_state import AdaptiveGraphState
from core.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    google_api_key=settings.GEMINI_API_KEY
)

hint_prompt = PromptTemplate(
    input_variables=["attempt_number", "student_answer", "correct_answer"],
    template="""
    You are an encouraging math tutor for young students. 
    The student gave the answer '{student_answer}', but the correct answer is '{correct_answer}'.
    This is their attempt number {attempt_number}.

    If attempt_number is 1: Give a very gentle, 1-sentence conceptual hint. Do NOT reveal the answer.
    If attempt_number is 2: Give a more specific 2-sentence explanation of the steps. Do NOT reveal the answer.

    Output only the hint text.
    """
)

# Connect the prompt to the Gemini model
hint_chain = hint_prompt | llm

def generate_scaffolded_hint(state: AdaptiveGraphState) -> dict:
    """Generates an AI-driven scaffolded hint for incorrect answers using Gemini with a fallback."""
    try:
        # Run the LangChain LLM to generate the hint
        response = hint_chain.invoke({
            "attempt_number": state["attempt_number"],
            "student_answer": state["student_answer"],
            "correct_answer": state["correct_answer"]
        })
        hint_text = response.content
    except Exception as e:
        logger.error(f"Gemini hint generation failed: {e}")
        # Pre-written hint fallback
        if state["attempt_number"] == 1:
            hint_text = "That's not quite right. Try taking a closer look at the problem and think about the steps carefully."
        else:
            hint_text = "Let's review the concepts. Remember to apply the correct operation and check your work!"

    hint_data = {
        "hint_level": state["attempt_number"],
        "content": hint_text
    }

    return {
        "hint_payload": hint_data,
        "attempt_number": state["attempt_number"] + 1
    }