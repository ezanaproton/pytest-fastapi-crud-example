import time


def test_root(test_client):
    response = test_client.get("/api/healthchecker")
    assert response.status_code == 200
    assert response.json() == {"message": "The API is LIVE!!"}


def test_create_get_user(test_client, user_payload):
    response = test_client.post("/api/users/", json=user_payload)
    response_json = response.json()
    assert response.status_code == 201

    # Get the created user
    response = test_client.get(f"/api/users/{user_payload['id']}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["Status"] == "Success"
    assert response_json["User"]["id"] == user_payload["id"]
    assert response_json["User"]["address"] == "123 Farmville"
    assert response_json["User"]["first_name"] == "John"
    assert response_json["User"]["last_name"] == "Doe"


def test_create_update_user(test_client, user_payload, user_payload_updated):
    response = test_client.post("/api/users/", json=user_payload)
    response_json = response.json()
    assert response.status_code == 201

    # Update the created user
    time.sleep(
        1
    )  # Sleep for 1 second to ensure updatedAt is different (datetime precision is low in SQLite)
    response = test_client.patch(
        f"/api/users/{user_payload['id']}", json=user_payload_updated
    )
    response_json = response.json()
    assert response.status_code == 202
    assert response_json["Status"] == "Success"
    assert response_json["User"]["id"] == user_payload["id"]
    assert response_json["User"]["address"] == "321 Farmville"
    assert response_json["User"]["first_name"] == "Jane"
    assert response_json["User"]["last_name"] == "Doe"
    assert response_json["User"]["activated"] is True
    assert (
        response_json["User"]["updatedAt"] is not None
        and response_json["User"]["updatedAt"] > response_json["User"]["createdAt"]
    )


def test_create_delete_user(test_client, user_payload):
    response = test_client.post("/api/users/", json=user_payload)
    response_json = response.json()
    assert response.status_code == 201

    # Delete the created user
    response = test_client.delete(f"/api/users/{user_payload['id']}")
    response_json = response.json()
    assert response.status_code == 202
    assert response_json["Status"] == "Success"
    assert response_json["Message"] == "User deleted successfully"

    # Get the deleted user
    response = test_client.get(f"/api/users/{user_payload['id']}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == f"No User with this id: `{user_payload['id']}` found"


def test_get_user_not_found(test_client, user_id):
    response = test_client.get(f"/api/users/{user_id}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == f"No User with this id: `{user_id}` found"


def test_create_user_wrong_payload(test_client):
    response = test_client.post("/api/users/", json={})
    assert response.status_code == 422


def test_update_user_wrong_payload(test_client, user_id, user_payload_updated):
    user_payload_updated["first_name"] = (
        True  # first_name should be a string not a boolean
    )
    response = test_client.patch(f"/api/users/{user_id}", json=user_payload_updated)
    assert response.status_code == 422
    response_json = response.json()
    assert response_json == {
        "detail": [
            {
                "type": "string_type",
                "loc": ["body", "first_name"],
                "msg": "Input should be a valid string",
                "input": True,
            }
        ]
    }


def test_update_user_doesnt_exist(test_client, user_id, user_payload_updated):
    response = test_client.patch(f"/api/users/{user_id}", json=user_payload_updated)
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == f"No User with this id: `{user_id}` found"


def test_create_update_user_status_wrong(test_client, user_payload, user_payload_updated):
    response = test_client.post("/api/users/", json=user_payload)
    response_json = response.json()
    assert response.status_code == 201

    time.sleep(1)
    response = test_client.patch(
        f"/api/users/{user_payload['id']}", json=user_payload_updated
    )
    assert response.status_code == 200


def test_pagination_boundary(test_client):
    # Create 15 users
    user_ids = []
    for i in range(15):
        payload = {
            "id": str(__import__('uuid').uuid4()),
            "first_name": f"User{i}",
            "last_name": "Test",
            "address": f"Address {i}",
            "activated": True
        }
        response = test_client.post("/api/users/", json=payload)
        assert response.status_code == 201
        user_ids.append(payload["id"])

    # Get page 1 (should be 0-9)
    response = test_client.get("/api/users/?page=1&limit=10")
    assert response.status_code == 200
    page1_users = response.json()["users"]
    assert len(page1_users) == 10
    page1_names = {u["first_name"] for u in page1_users}
    expected_page1 = {f"User{i}" for i in range(10)}
    assert page1_names == expected_page1

    # Get page 2 (should be 10-14)
    response = test_client.get("/api/users/?page=2&limit=10")
    assert response.status_code == 200
    page2_users = response.json()["users"]
    assert len(page2_users) == 5
    page2_names = {u["first_name"] for u in page2_users}
    expected_page2 = {f"User{i}" for i in range(10, 15)}
    assert page2_names == expected_page2


def test_create_user_empty_first_name(test_client):
    payload = {
        "id": str(__import__('uuid').uuid4()),
        "first_name": "",
        "last_name": "Test",
        "address": "123 Test St",
        "activated": True
    }
    response = test_client.post("/api/users/", json=payload)
    assert response.status_code == 400
    assert "First name cannot be empty" in response.json()["detail"]
