def test_get_all_tickets_with_empty_db_returns_empty_list(client):
    response = client.get("/tickets")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_tickets_returns_list_of_tickets(client, two_giveaways, two_participants, two_tickets):
    response = client.get("/tickets")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {"id": 1,
         "giveaway_id": 1,
         "participant_id": 1},
        {"id": 2,
         "giveaway_id": 1,
         "participant_id": 2}
    ]