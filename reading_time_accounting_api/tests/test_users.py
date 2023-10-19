import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_user_authentication():
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

    response = client.get("/api/user/me/")
    assert response.status_code == 200
    assert response.data["email"] == user_data["email"]
