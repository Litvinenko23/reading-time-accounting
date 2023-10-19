import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from book.models import Book


@pytest.mark.django_db
def test_book_api():
    client = APIClient()
    user_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    user = get_user_model().objects.create_user(**user_data)

    response = client.post("/api/user/token/", user_data)
    assert response.status_code == 200
    assert "access" in response.data

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "publication_year": 2020,
        "short_description": "Short description",
        "full_description": "Full description",
    }
    response = client.post("/api/book/books/", book_data, format="json")
    assert response.status_code == 201

    book_id = response.data["id"]
    response = client.get(f"/api/book/books/{book_id}/")
    assert response.status_code == 200
    assert response.data["title"] == book_data["title"]

    response = client.get("/api/book/books/")
    assert response.status_code == 200
    assert len(response.data) == 1

    updated_data = {"title": "Updated Book Title"}
    response = client.patch(f"/api/book/books/{book_id}/", updated_data, format="json")
    assert response.status_code == 200
    assert response.data["title"] == updated_data["title"]

    response = client.delete(f"/api/book/books/{book_id}/")
    assert response.status_code == 204

    assert not Book.objects.filter(id=book_id).exists()
