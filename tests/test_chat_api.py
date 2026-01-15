from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_endpoint():
    response = client.post(
        "/chat",
        json={"message": "2 bhk flats in Pune"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "filters_used" in data