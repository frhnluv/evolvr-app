import pytest
from services.report_service import get_student_mastery_dashboard
from fastapi import HTTPException
from unittest.mock import MagicMock

def test_get_student_mastery_dashboard_at_risk(mocker):
    mock_supabase = mocker.patch("services.report_service.supabase")
    # Mock student response
    mock_student_response = MagicMock()
    mock_student_response.data = [{
        "student_id": "test-student-1",
        "User": {"surname": "Doe", "other_names": "John"}
    }]
    
    # Mock progress response
    mock_progress_response = MagicMock()
    mock_progress_response.data = [
        {"progress_id": "p1", "strand": "Algebra", "sub_strand": "Linear", "mastery_level": 25.0, "updated_at": "2024-01-01T00:00:00Z"},
        {"progress_id": "p2", "strand": "Geometry", "sub_strand": "Shapes", "mastery_level": 80.0, "updated_at": "2024-01-01T00:00:00Z"}
    ]
    
    # Configure mock chain
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [
        mock_student_response,
        mock_progress_response
    ]
    
    result = get_student_mastery_dashboard("test-student-1")
    
    assert result["student_name"] == "John Doe"
    assert len(result["mastery_records"]) == 2
    # The student is at risk because one mastery level is 25.0 (< 30.0)
    assert result["at_risk"] is True

def test_get_student_mastery_dashboard_not_found(mocker):
    mock_supabase = mocker.patch("services.report_service.supabase")
    mock_student_response = MagicMock()
    mock_student_response.data = []
    
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_student_response
    
    with pytest.raises(HTTPException) as exc:
        get_student_mastery_dashboard("non-existent-student")
        
    assert exc.value.status_code == 404
