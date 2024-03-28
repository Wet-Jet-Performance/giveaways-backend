def test_get_all_participants_with_empty_db_returns_empty_list(client):
    response = client.get("/participants")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_participants_returns_list_of_participants(client, two_participants):
    response = client.get("/participants")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {"id": 1,
         "name": "Participant 1",
         "phone_number": "(123)456-7890",
         "email": "participant1@email.com"},
        {"id": 2,
         "name": "Participant 2",
         "phone_number": "(123)456-7891",
         "email": "participant2@email.com"}
    ]