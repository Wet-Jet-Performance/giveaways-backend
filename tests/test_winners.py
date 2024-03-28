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