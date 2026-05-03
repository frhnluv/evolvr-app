import pytest
from fastapi.testclient import TestClient
from main import app
from core.security import get_current_user
import uuid

# Mock the current user dependency globally for all API tests
def mock_get_current_user():
    return {"id": str(uuid.uuid4()), "email": "test@example.com", "role": "teacher"}

app.dependency_overrides[get_current_user] = mock_get_current_user

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
