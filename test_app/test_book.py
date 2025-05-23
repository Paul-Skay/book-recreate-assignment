from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_add_book():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    data = response.json()
    assert data["message"] == "Book added successfully"
    assert data["data"]["title"] == "Johny bravo"


def test_get_book_by_id():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    add_book_data = response.json()
    book_id = add_book_data['data']['id']
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 200
    assert get_book_data['id'] == book_id


def test_get_book_by_id_not_found():
    book_id = 1
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 404
    assert get_book_data['detail'] == "book not found."


def test_update_book():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    book_id = response.json()['data']['id']
    update_payload = {
        "title": "Forever 21",
        "author": "Jane Doe",
        "year": 1990,
        "pages": 1500,
        "language": "French"
    }
    update_response = client.put(f"/books/{book_id}", json=update_payload)
    update_book_data = update_response.json()
    assert update_response.status_code == 200
    assert update_book_data["message"] == "Book updated successfully"
    assert update_book_data["data"]["title"] == "Forever 21"
    assert update_book_data["data"]["author"] == "Jane Doe"
    assert update_book_data["data"]["year"] == 1990
    assert update_book_data["data"]["pages"] == 1500
    assert update_book_data["data"]["language"] == "French"


def test_update_book_not_found():
    book_id = 100
    payload = {
        "title": "Forever 21",
        "author": "Jane Doe",
        "year": 1990,
        "pages": 1500,
        "language": "French"
    }
    response = client.put(f"/books/{book_id}", json=payload)
    assert response.status_code == 404
    update_book_data = response.json()
    assert update_book_data["detail"] == f"Book with id: {book_id} not found"


def test_delete_book():
    book_data = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }

    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()['data']['id']
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"


def test_delete_book_not_found():
    book_id = 100
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Book with id: {book_id} not found"

