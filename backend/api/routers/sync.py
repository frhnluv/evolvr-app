# api/routers/sync.py
from fastapi import APIRouter, Depends, HTTPException
from core.database import supabase
from core.security import get_current_user
from api.schemas import SyncBatchPayload, EngineFeedbackResponse, HintPayload
from services.adaptive_engine.graph import adaptive_engine
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/outbox", summary="Process batched offline interactions")
async def sync_offline_outbox(
        payload: SyncBatchPayload,
        current_user = Depends(get_current_user)
):
    """
    Receives queued learning transactions, saves them to the database,
    and runs them through the LangGraph Adaptive Engine .
    """
    successful_syncs = []
    failed_syncs = []
    engine_feedbacks = {}  # We will return the engine's feedback for each question

    for record in payload.records:
        try:
            # 1. Fetch the correct answer from the database for the engine to evaluate
            question_query = supabase.table("questions").select("content_payload").eq("id", str(record.question_id)).execute()
            if not question_query.data:
                logger.error(f"Question {record.question_id} not found.")
                correct_answer = ""
            else:
                payload_data = question_query.data[0].get("content_payload", {})
                correct_answer = payload_data.get("answer", "")

            # 2. Setup the state for the LangGraph Engine
            initial_state = {
                "student_id": str(payload.student_id),
                "skill_id": str(record.skill_id),
                "question_id": str(record.question_id),
                "student_answer": record.student_answer,
                "correct_answer": correct_answer,
                "attempt_number": record.attempt_number,
                "ability_level": record.ability_level,
                "confidence_score": 0.5,  # In production, fetch this from `student_skill_metrics`
                "hint_payload": None,
                "next_question_id": None
            }

            # 3. Run the Engine!
            final_state = adaptive_engine.invoke(initial_state)

            # 4. Save the student's raw response to Supabase
            response_data = {
                "id": str(record.id),
                "lesson_session_id": str(payload.session_id),
                "question_id": str(record.question_id),
                "attempt_number": record.attempt_number,
                "is_correct": final_state["is_correct"],
                "interaction_data": {"student_answer": record.student_answer},
                "recorded_time": record.recorded_at.isoformat(),
                "time_spent_seconds": record.time_spent_seconds,
                "hint_used_id": record.hint_used_id
            }
            supabase.table("responses").upsert(response_data).execute()

            # 5. Format the feedback to send back to the Flutter app
            feedback = EngineFeedbackResponse(
                is_correct=final_state["is_correct"],
                updated_ability=final_state["ability_level"],
                next_action="hint" if final_state.get("hint_payload") else "new_question",
                hint=HintPayload(**final_state["hint_payload"]) if final_state.get("hint_payload") else None,
                next_question_id=final_state.get("next_question_id")
            )

            # Store it using the record ID so the mobile app knows which response this feedback belongs to
            engine_feedbacks[str(record.id)] = feedback
            successful_syncs.append(str(record.id))

            # 6. Update the student's new ability/confidence in the DB (BKT Tracking)
            metrics_data = {
                "student_id": str(payload.student_id),
                "skill_id": str(record.skill_id),
                "ability_level": final_state["ability_level"],
                "mastery_probability": final_state.get("confidence_score", 0.0),
                "last_assessed": "now()"
            }
            supabase.table("student_skill_metrics").upsert(metrics_data, on_conflict="student_id, skill_id").execute()

        except Exception as e:
            logger.error(f"Failed to sync record {record.id}: {str(e)}")
            failed_syncs.append({"id": str(record.id), "error": str(e)})

    return {
        "message": "Sync processed",
        "synced_count": len(successful_syncs),
        "failed_count": len(failed_syncs),
        "synced_ids": successful_syncs,
        "engine_feedback": engine_feedbacks,  # Sends all the hints and next steps back!
        "failed_details": failed_syncs
    }