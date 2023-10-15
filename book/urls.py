from django.urls import path, include
from rest_framework.routers import DefaultRouter

from book.views import BookViewSet, ReadingSessionViewSet


router = DefaultRouter()
router.register("books", BookViewSet)
router.register("reading-sessions", ReadingSessionViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "book"
