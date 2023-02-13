from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


mock_datalogger = {
    "1609461880000": {"precip": 0.0, "temp": -2.2, "hum": 92.5},
    "1609530282000": {"precip": 0.0, "temp": -0.4, "hum": 87.0},
}


def test_url_data():
    response = client.get("/api/data")
    assert response.status_code == 200


def test_url_summary():
    response = client.get("/api/summary")
    assert response.status_code == 200
