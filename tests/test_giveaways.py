def test_get_all_giveaways_with_empty_db_returns_empty_list(client):
    response = client.get("/giveaways")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_giveaways_returns_list_of_giveaways(client, two_giveaways):
    response = client.get("/giveaways")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {"id": 1,
         "name": "Giveaway 1",
         "start_date": "Thu, 28 Mar 2024 00:00:00 GMT",
         "end_date": "Fri, 29 Mar 2024 00:00:00 GMT"},
        {"id": 2,
         "name": "Giveaway 2",
         "start_date": "Sun, 21 Apr 2024 00:00:00 GMT",
         "end_date": "Tue, 23 Apr 2024 00:00:00 GMT"}
    ]

def test_create_two_giveaways(client):
    response1 = client.post("/giveaways", json={
        "name": "New Giveaway 1",
        "start_date": "July 1, 2024",
        "end_date": "July 7, 2024"
    })
    response_body1 = response1.get_json()

    response2 = client.post("/giveaways", json={
        "name": "New Giveaway 2",
        "start_date": "August 1, 2024",
        "end_date": "August 7, 2024"
    })
    response_body2 = response2.get_json()

    assert response1.status_code == 201
    assert "success" in response_body1["msg"].lower()
    assert "1" in response_body1["msg"]

    assert response2.status_code == 201
    assert "success" in response_body2["msg"].lower()
    assert "2" in response_body2["msg"]

    #ensure new data is in database
    response3 = client.get("/giveaways")
    response_body3 = response3.get_json()

    assert response3.status_code == 200
    assert response_body3 == [
        {"id": 1,
         "name": "New Giveaway 1",
         "start_date": "Mon, 01 Jul 2024 00:00:00 GMT",
         "end_date": "Sun, 07 Jul 2024 00:00:00 GMT"},
        {"id": 2,
         "name": "New Giveaway 2",
         "start_date": "Thu, 01 Aug 2024 00:00:00 GMT",
         "end_date": "Wed, 07 Aug 2024 00:00:00 GMT"}
    ]

def test_get_giveaway_by_id_returns_correct_giveaway(client, two_giveaways):
    response1 = client.get("/giveaways/1")
    response_body1 = response1.get_json()

    response2 = client.get("/giveaways/2")
    response_body2 = response2.get_json()

    assert response1.status_code == 200
    assert response_body1 == {
        "id": 1,
        "name": "Giveaway 1",
        "start_date": "Thu, 28 Mar 2024 00:00:00 GMT",
        "end_date": "Fri, 29 Mar 2024 00:00:00 GMT"
        }
    assert response2.status_code == 200
    assert response_body2 == {
        "id": 2,
        "name": "Giveaway 2",
        "start_date": "Sun, 21 Apr 2024 00:00:00 GMT",
        "end_date": "Tue, 23 Apr 2024 00:00:00 GMT"
        }

def test_get_giveaway_participants_returns_list_of_participants(client, two_giveaways, two_participants, two_tickets):
    response = client.get("/giveaways/1/participants")
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

def test_update_giveaway(client, two_giveaways):
    response1 = client.put("/giveaways/1", json={
        "name": "New Giveaway 1",
        "start_date": "July 1, 2024",
        "end_date": "July 7, 2024"
    })
    response_body1 = response1.get_json()

    assert response1.status_code == 200
    assert "success" in response_body1["msg"].lower()
    assert "1" in response_body1["msg"]

    #ensure new data is in database
    response2 = client.get("/giveaways")
    response_body2 = response2.get_json()

    assert response2.status_code == 200
    #note - updated item placed at end of list
    assert response_body2 == [
        {"id": 2,
         "name": "Giveaway 2",
         "start_date": "Sun, 21 Apr 2024 00:00:00 GMT",
         "end_date": "Tue, 23 Apr 2024 00:00:00 GMT"},
        {"id": 1,
         "name": "New Giveaway 1",
         "start_date": "Mon, 01 Jul 2024 00:00:00 GMT",
         "end_date": "Sun, 07 Jul 2024 00:00:00 GMT"}
    ]

def test_delete_giveaway(client, two_giveaways):
    response1 = client.delete("/giveaways/1")
    response_body1 = response1.get_json()

    assert response1.status_code == 200
    assert "success" in response_body1["msg"].lower()
    assert "1" in response_body1["msg"]

    #ensure data deleted from database
    response2 = client.get("/giveaways")
    response_body2 = response2.get_json()

    assert response2.status_code == 200
    assert response_body2 == [{
        "id": 2,
        "name": "Giveaway 2",
        "start_date": "Sun, 21 Apr 2024 00:00:00 GMT",
        "end_date": "Tue, 23 Apr 2024 00:00:00 GMT"
        }]