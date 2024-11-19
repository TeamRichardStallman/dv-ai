from fastapi.testclient import TestClient

client = TestClient()


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World"}
