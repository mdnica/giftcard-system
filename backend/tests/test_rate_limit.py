def test_rate_limit(client):
    for _ in range(6):
        res = client.post("/giftcards/redeem", json={"code": "FAKE"})
    assert res.status_code == 429
