def test_register(client):
    response = client.post("/api/register", json={
        "username": "bob1",
        "password": "pass",
        "email": "bob1@example.com",
        "name": "Bobby"
    })

    assert response.status_code == 200
    assert response.json["message"] == "registered successfully"

def test_unsuccessful_register(client):
    response = client.post("/api/register", json={
        "username": "bob1"
    })

    assert response.status_code == 400
    assert b"registration unsuccessful" in response.data