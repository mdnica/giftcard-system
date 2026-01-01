def test_redeem_invalid_card(client, auth_headers):
    response = client.post(
        "/giftcards/redeem",
        json={"code": "INVALID"},
        headers=auth_headers,
    )
    assert response.status_code in (400, 404)
