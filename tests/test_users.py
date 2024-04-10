from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app import app


client = TestClient(app)


@patch('apis.users.add_user')
def test_add_user(mock_add_user):
    mock_add_user.return_value = {"name": "Test01", "group_id": 1}
    response = client.post("/addUser", json={"name": "Test01", "group_id": 1})
    assert response.status_code == 200
