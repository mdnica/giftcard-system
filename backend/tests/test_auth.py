def test_login_success(client):
    response = client.post(
        "/auth/token",
        data={"username": "admin@test.com", "password": "admin123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
