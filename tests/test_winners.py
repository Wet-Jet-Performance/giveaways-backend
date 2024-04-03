def test_get_all_winners_with_empty_db_returns_empty_list(client):
    response = client.get("/winners")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_winners_returns_list_of_winners(client, two_giveaways, two_participants, two_winners):
    response = client.get("/winners")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {"id": 1,
         "giveaway_id": 1,
         "participant_id": 1},
        {"id": 2,
         "giveaway_id": 2,
         "participant_id": 2}
    ]

def test_create_two_winners(client, two_giveaways, two_participants):
    response1 = client.post("/winners", json={
        "giveaway_id": 1,
        "participant_id": 1
    })
    response_body1 = response1.get_json()

    response2 = client.post("/winners", json={
        "giveaway_id": 2,
        "participant_id": 2
    })
    response_body2 = response2.get_json()

    assert response1.status_code == 201
    assert "success" in response_body1["msg"].lower()
    assert "1" in response_body1["msg"]

    assert response2.status_code == 201
    assert "success" in response_body2["msg"].lower()
    assert "2" in response_body2["msg"]

    # ensure winners added to table
    response3 = client.get("/winners")
    response_body3 = response3.get_json()

    assert response3.status_code == 200
    assert response_body3 == [
        {"id": 1,
         "giveaway_id": 1,
         "participant_id": 1},
        {"id": 2,
         "giveaway_id": 2,
         "participant_id": 2}
    ]