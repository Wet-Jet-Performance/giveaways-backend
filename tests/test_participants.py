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

def test_create_two_participants(client):
    response1 = client.post("/participants", json={
        "name": "New Participant 1",
        "phone_number": "(123)456-7890",
        "email": "newparticipant1@email.com"
    })
    response_body1 = response1.get_json()

    response2 = client.post("/participants", json={
        "name": "New Participant 2",
        "phone_number": "(123)456-7891",
        "email": "newparticipant2@email.com"
    })
    response_body2 = response2.get_json()

    assert response1.status_code == 201
    assert "success" in response_body1["msg"].lower()
    assert "1" in response_body1["msg"]

    assert response2.status_code == 201
    assert "success" in response_body2["msg"].lower()
    assert "2" in response_body2["msg"]

    #ensure new data is in database
    response3 = client.get("/participants")
    response_body3 = response3.get_json()

    assert response3.status_code == 200
    assert response_body3 == [
        {"id": 1,
         "name": "New Participant 1",
         "phone_number": "(123)456-7890",
         "email": "newparticipant1@email.com"},
        {"id": 2,
         "name": "New Participant 2",
         "phone_number": "(123)456-7891",
         "email": "newparticipant2@email.com"}
    ]

def test_get_participant_by_id_returns_correct_participant(client, two_participants):
    response1 = client.get("/participants/1")
    response_body1 = response1.get_json()

    assert response1.status_code == 200
    assert response_body1 == {
        "id": 1,
        "name": "Participant 1",
        "phone_number": "(123)456-7890",
        "email": "participant1@email.com"
    }

    response2 = client.get("/participants/2")
    response_body2 = response2.get_json()

    assert response2.status_code == 200
    assert response_body2 == {
        "id": 2,
        "name": "Participant 2",
        "phone_number": "(123)456-7891",
        "email": "participant2@email.com"
    }