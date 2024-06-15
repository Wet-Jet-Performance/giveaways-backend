def test_get_all_photos_with_empty_db_returns_empty_list(client):
    response = client.get("/photos")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_photos_returns_list_of_photos(client, two_giveaways, two_photos):
    response = client.get("/photos")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {"id": 1,
         "cloudflare_id": "1"},
        {"id": 2,
         "cloudflare_id": "2"}
    ]

def test_create_two_photos(client, two_giveaways):
    response1 = client.post("/photos", json={
        "cloudflare_id": "1",
        "giveaway_id": 1,
    })
    response_body1 = response1.get_json()

    response2 = client.post("/photos", json={
        "cloudflare_id": "2",
        "giveaway_id": 2,
    })
    response_body2 = response2.get_json()

    assert response1.status_code == 201
    assert "success" in response_body1["msg"].lower()
    assert response_body1["id"] == 1

    assert response2.status_code == 201
    assert "success" in response_body2["msg"].lower()
    assert response_body2["id"] == 2

    # ensure new data is in database
    response3 = client.get("/photos")
    response_body3 = response3.get_json()

    assert response3.status_code == 200
    assert response_body3 == [
        {"id": 1,
         "cloudflare_id": "1"},
        {"id": 2,
         "cloudflare_id": "2"}
    ]
