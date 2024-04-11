from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app


client = TestClient(app)


@patch('apis.users.can_join_group')
@patch('database.SessionLocal')
def test_add_user_without_group(mock_session_local, mock_can_join_group):
    mock_can_join_group.return_value = True
    response = client.post("/addUser", json={"name": "Test00", "group_id": None})
    assert response.status_code == 200


@patch('apis.users.can_join_group')
@patch('database.SessionLocal')
def test_add_user_with_valid_group(mock_session_local, mock_can_join_group):
    mock_can_join_group.return_value = True
    response = client.post("/addUser", json={"name": "Test00", "group_id": 1})
    assert response.status_code == 200


@patch('apis.users.can_join_group')
def test_add_user_to_deactivated_group(mock_can_join_group):
    mock_can_join_group.return_value = False
    response = client.post("/addUser", json={"name": "Test01", "group_id": 22})
    assert response.status_code == 400


@patch('database.SessionLocal')
@patch('apis.users.get_single_group')
def test_add_user_to_inexisted_group(mock_get_single_group, mock_session_local):
    mock_get_single_group.return_value = None
    mock_session_local.query.return_value.filter_by.return_value.first.return_value = None
    response = client.post("/addUser", json={"name": "Test02", "group_id": 100})
    assert response.status_code == 404