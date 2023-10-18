import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from book.models import ReadingSession, Book


@pytest.mark.django_db
def test_reading_sessions():
    client = APIClient()
    user_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    user = get_user_model().objects.create_user(**user_data)

    # Obtain an access token for the test user
    response = client.post("/api/user/token/", user_data)
    assert response.status_code == 200
    access_token = response.data.get("access")
    assert access_token is not None  # Ensure the access token is obtained successfully

    # Create a book
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "publication_year": 2020,
        "short_description": "Short description",
        "full_description": "Full description",
    }
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = client.post("/api/book/books/", book_data, format="json")
    book_id = response.data.get("id")

    # assert book_id is not None

    # Start a reading session
    response = client.post(f"/api/book/start-reading-session/{book_id}/")
    # assert response.status_code == 201
    assert ReadingSession.objects.filter(book_id=book_id, user=user, end_time__isnull=True).count() == 1

    # Attempt to start another session with the same book (should fail)
    response = client.post(f"/api/book/start-reading-session/{book_id}/")
    assert response.status_code == 400

    # End the reading session
    response = client.post(f"/api/book/end-reading-session/{book_id}/")
    assert response.status_code == 200
    session = ReadingSession.objects.get(book_id=book_id, user=user, end_time__isnull=False)
    assert session.duration.total_seconds() > 0
