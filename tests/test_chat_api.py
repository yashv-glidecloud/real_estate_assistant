from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_endpoint_basic():
    response = client.post(
        "/chat",
        json={"message": "2 bhk flats in Pune"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "filters_used" in data
    assert "results" in data


def test_chat_followup_memory():
    session_id = "test_session"

    client.post(
        "/chat",
        json={"message": "2 bhk flats in Pune", "session_id": session_id}
    )

    response = client.post(
        "/chat",
        json={"message": "under 80 lakhs", "session_id": session_id}
    )

    data = response.json()
    assert data["filters_used"]["bhk"] == 2
    assert data["filters_used"]["max_price_lakhs"] == 80


def test_chat_no_results_response():
    response = client.post(
        "/chat",
        json={"message": "10 bhk flats in Mars"}
    )

    data = response.json()
    assert data["results"] == []
    assert "No properties found" in data["answer"]