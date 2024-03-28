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