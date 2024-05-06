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
        {"giveaway_id": 1,
         "giveaway_name": "Giveaway 1",
         "id": 1,
         "participant_email": "participant1@email.com",
         "participant_id": 1,
         "participant_name": "Participant 1",
         "participant_phone": "(123)456-7890"},
        {"giveaway_id": 1,
         "giveaway_name": "Giveaway 1",
         "id": 2,
         "participant_email": "participant2@email.com",
         "participant_id": 2,
         "participant_name": "Participant 2",
         "participant_phone": "(123)456-7891"}
    ]

def test_create_two_tickets(client, two_giveaways, two_participants):
    response1 = client.post("/tickets", json={
        "giveaway_id": 1,
        "participant_id": 1
    })
    response_body1 = response1.get_json()

    response2 = client.post("/tickets", json={
        "giveaway_id": 1,
        "participant_id": 2
    })
    response_body2 = response2.get_json()

    assert response1.status_code == 201
    assert "success" in response_body1["msg"].lower()

    assert response2.status_code == 201
    assert "success" in response_body2["msg"].lower()

    # ensure new ticket in database
    response3 = client.get("/tickets")
    response_body3 = response3.get_json()

    assert response3.status_code == 200
    assert response_body3 == [
        {"giveaway_id": 1,
         "giveaway_name": "Giveaway 1",
         "id": 1,
         "participant_email": "participant1@email.com",
         "participant_id": 1,
         "participant_name": "Participant 1",
         "participant_phone": "(123)456-7890"},
        {"giveaway_id": 1,
         "giveaway_name": "Giveaway 1",
         "id": 2,
         "participant_email": "participant2@email.com",
         "participant_id": 2,
         "participant_name": "Participant 2",
         "participant_phone": "(123)456-7891"}
    ]

def test_bulk_create_two_tickets(client, two_giveaways, two_participants):
    response1 = client.post("/tickets", json={
        "giveaway_id": 1,
        "participant_id": 1,
        "number_of_tickets": 2
    })
    response_body1 = response1.get_json()

    assert response1.status_code == 201
    assert "success" in response_body1["msg"].lower()

    # ensure new tickets in database
    response2 = client.get("/tickets")
    response_body2 = response2.get_json()

    assert response2.status_code == 200
    assert response_body2 == [
        {"giveaway_id": 1,
         "giveaway_name": "Giveaway 1",
         "id": 1,
         "participant_email": "participant1@email.com",
         "participant_id": 1,
         "participant_name": "Participant 1",
         "participant_phone": "(123)456-7890"},
        {"giveaway_id": 1,
         "giveaway_name": "Giveaway 1",
         "id": 2,
         "participant_email": "participant1@email.com",
         "participant_id": 1,
         "participant_name": "Participant 1",
         "participant_phone": "(123)456-7890"},
    ]

def test_get_one_ticket_returns_correct_ticket(client, two_giveaways, two_participants, two_tickets):
    response = client.get("/tickets/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
            "giveaway_id": 1,
            "giveaway_name": "Giveaway 1",
            "id": 1,
            "participant_email": "participant1@email.com",
            "participant_id": 1,
            "participant_name": "Participant 1",
            "participant_phone": "(123)456-7890"
        }

def test_delete_ticket(client, two_giveaways, two_participants, two_tickets):
    response1 = client.delete("/tickets/1")
    response_body1 = response1.get_json()

    assert response1.status_code == 200
    assert "success" in response_body1["msg"].lower()
    assert "1" in response_body1["msg"]

    # ensure ticket deleted from database
    response2 = client.get("/tickets")
    response_body2 = response2.get_json()

    assert response2.status_code == 200
    assert response_body2 == [{
        "giveaway_id": 1,
        "giveaway_name": "Giveaway 1",
        "id": 2,
        "participant_email": "participant2@email.com",
        "participant_id": 2,
        "participant_name": "Participant 2",
        "participant_phone": "(123)456-7891"
    }]