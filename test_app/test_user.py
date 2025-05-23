from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_user():
    user_data = {
        "name": "John Doe",
        "email": "john.doe@gmail.com",
        "password": "john12345",
        "age": 25,
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    add_user_data = response.json()
    assert add_user_data["message"] == "user added successfully"
    assert add_user_data["data"]["name"] == "John Doe"
    assert add_user_data["data"]["email"] == "john.doe@gmail.com"
    assert add_user_data["data"]["age"] == 25
    assert isinstance(add_user_data["data"], dict)


def test_add_user_missing_fields():
    user_data = {
        "name": "John Doe",

    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 422
    add_user_data = response.json()
    assert add_user_data["detail"][0]["msg"] == "field required"
    assert add_user_data["detail"][0]["loc"] == ["body", "email"]
    assert add_user_data["detail"][0]["type"] == "missing"
    assert add_user_data["detail"][1]["msg"] == "field required"
    assert add_user_data["detail"][1]["loc"] == ["body", "password"]


def test_add_user_short_password():
    user_data = {
        "name": "Jane Doe",
        "email": "jane.doe@gmail.com",
        "password": "jane",
        "age": 20,
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 422
    assert "at least 8 characters" in response.json()["detail"][0]["msg"]


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["message"] == "users retrieved successfully"


def test_get_user_by_id():
    user_data = {
        "name": "Jane Doe",
        "email": "jane.doe@gmail.com",
        "password": "jane",
        "age": 20,
    }
    response = client.post("/users", json=user_data)    
    user_id = response.json()["data"]["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["message"] == "user retrieved successfully"
    assert user_data["data"]["id"] == user_id
    assert user_data["data"]["name"] == "Jane Doe"
    assert isinstance(user_data["data"], dict)


def test_get_user_by_id_not_found():
    user_id = 100
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "user not found."


def test_update_user():
    user_data = {
        "name": "John Doe",
        "email": "john.doe@gmail.com",
        "password": "john12345",
        "age": 25,
    }
    create_response = client.post("/users/", json=user_data)
    user_id = create_response.json()['data']["id"]
    updated_user_data = {
        "name": "Jane Doe",
        "email": "jane.doe@gmail.com",
        "age": 36,
    }
    response = client.put(f"/users/{user_id}", json=updated_user_data)
    assert response.status_code == 200
    assert response.json()['data']["name"] == "Jane Doe"
    assert response.json()["message"] == "user updated successfully"


def test_update_user_not_found():
    user_id = 100
    user_data = {
        "name": "Jane Doe",
        "email": "jane.doe@gmail.com",
        "age": 36,
    }
    response = client.put(f"/users/{user_id}", json=user_data)
    assert response.status_code == 404
    assert response.json()["detail"] == f"user with id: {user_id} not found"


def test_delete_user():
    user_data = {
        "name": "Jane Doe",
        "email": "jane.doe@gmail.com",
        "password": "jane12345",
        "age": 20,
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["data"]["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "user deleted successfully"


def test_delete_user_not_found():
    user_id = 100
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"user with id: {user_id} not found"
