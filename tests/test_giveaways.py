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
         "start_date": "March 28, 2024",
         "end_date": "March 29, 2024"},
        {"id": 2,
         "name": "Giveaway 2",
         "start_date": "April 21, 2024",
         "end_date": "April 23, 2024"}
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

    # ensure new data is in database
    response3 = client.get("/giveaways")
    response_body3 = response3.get_json()

    assert response3.status_code == 200
    assert response_body3 == [
        {"id": 1,
         "name": "New Giveaway 1",
         "start_date": "July 1, 2024",
         "end_date": "July 7, 2024"},
        {"id": 2,
         "name": "New Giveaway 2",
         "start_date": "August 1, 2024",
         "end_date": "August 7, 2024"}
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
        "start_date": "March 28, 2024",
        "end_date": "March 29, 2024"
        }
    assert response2.status_code == 200
    assert response_body2 == {
        "id": 2,
        "name": "Giveaway 2",
        "start_date": "April 21, 2024",
        "end_date": "April 23, 2024"
        }

def test_get_giveaway_tickets_returns_list_of_tickets(client, two_giveaways, two_participants, two_tickets):
    response = client.get("/giveaways/1/tickets")
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

def test_get_giveaway_tickets_returns_list_of_tickets(client, two_giveaways, two_participants, two_winners):
    response = client.get("/giveaways/1/winners")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {"id": 1,
         "giveaway_id": 1,
         "participant_id": 1}
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

    # ensure new data is in database
    response2 = client.get("/giveaways")
    response_body2 = response2.get_json()

    assert response2.status_code == 200
    # note - updated item placed at end of list
    assert response_body2 == [
        {"id": 2,
         "name": "Giveaway 2",
         "start_date": "April 21, 2024",
         "end_date": "April 23, 2024"},
        {"id": 1,
         "name": "New Giveaway 1",
         "start_date": "July 1, 2024",
         "end_date": "July 7, 2024"}
    ]

def test_delete_giveaway_deletes_giveaway_and_its_tickets_and_winners(client, two_giveaways, two_participants, two_tickets, two_winners):
    response1 = client.delete("/giveaways/1")
    response_body1 = response1.get_json()

    assert response1.status_code == 200
    assert "success" in response_body1["msg"].lower()
    assert "1" in response_body1["msg"]

    # ensure data deleted from database
    response2 = client.get("/giveaways")
    response_body2 = response2.get_json()

    assert response2.status_code == 200
    assert response_body2 == [{
        "id": 2,
        "name": "Giveaway 2",
        "start_date": "April 21, 2024",
        "end_date": "April 23, 2024"
        }]
    
    # ensure tickets deleted
    response2 = client.get("/tickets")
    response_body2 = response2.get_json()

    assert response2.status_code == 200
    assert response_body2 == []

    # ensure winner deleted
    response3 = client.get("/winners")
    response_body3 = response3.get_json()

    assert response3.status_code == 200
    assert response_body3 == [{
        "id": 2,
        "giveaway_id": 2, 
        "participant_id": 2
    }]