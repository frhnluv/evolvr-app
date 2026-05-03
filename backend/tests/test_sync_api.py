import pytest
from unittest.mock import MagicMock, patch

def test_sync_offline_outbox(client, mocker):
    mock_invoke = mocker.patch("api.routers.sync.adaptive_engine.invoke")
    
    mock_invoke.return_value = {
        "is_correct": True,
        "ability_level": 0.8,
        "next_question_id": "123e4567-e89b-12d3-a456-426614174001",
        "hint_payload": None,
        "attempt_number": 1
    }
    
    # Also patch the record creation and question fetch
    mock_db = mocker.patch("api.routers.sync.supabase")
    # Upsert response
    mock_db.table.return_value.upsert.return_value.execute.return_value = MagicMock()
    # Select question
    mock_question_res = MagicMock()
    mock_question_res.data = [{"answer": "4"}]
    mock_db.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_question_res
        
    payload = {
        "sessionId": "123e4567-e89b-12d3-a456-426614174000",
        "records": [
            {
                "id": "123e4567-e89b-12d3-a456-426614174002",
                "studentId": "123e4567-e89b-12d3-a456-426614174003",
                "questionId": "123e4567-e89b-12d3-a456-426614174004",
                "skillId": "123e4567-e89b-12d3-a456-426614174005",
                "studentAnswer": "4",
                "attemptNumber": 1,
                "abilityLevel": 0.5,
                "recordedAt": "2024-01-01T00:00:00Z"
            }
        ]
    }
    
    response = client.post("/api/sync/outbox", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Sync processed"
    assert len(data["engine_feedback"]) == 1
    
    feedback = data["engine_feedback"]["123e4567-e89b-12d3-a456-426614174002"]
    assert feedback["isCorrect"] is True
    assert feedback["nextAction"] == "new_question"
