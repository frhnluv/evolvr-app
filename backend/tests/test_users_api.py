import pytest
from unittest.mock import MagicMock

def test_get_user_success(client, mocker):
    mock_supabase = mocker.patch("services.user_service.supabase")
    mock_response = MagicMock()
    mock_response.data = [{
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "surname": "Doe",
        "other_names": "John",
        "email": "john@example.com",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }]
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    response = client.get("/api/users/john@example.com")
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "john@example.com"
    assert data["surname"] == "Doe"

def test_get_user_not_found(client, mocker):
    mock_supabase = mocker.patch("services.user_service.supabase")
    mock_response = MagicMock()
    mock_response.data = []
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    response = client.get("/api/users/nonexistent@example.com")
    
    assert response.status_code == 404
