from django.urls import path, include
from rest_framework.routers import DefaultRouter

from book.views import BookViewSet, ReadingSessionViewSet
from book.views import StartReadingSession, EndReadingSession


router = DefaultRouter()
router.register("books", BookViewSet)
router.register("reading-sessions", ReadingSessionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # path("books/<int:pk>/start-reading-session/", ReadingSessionViewSet.as_view({"post": "start_reading_session"}), name="start-reading-session"),

    # path("books/<int:pk>/start-reading-session/", ReadingSessionViewSet.as_view({"post": "start_reading_session"}),
    #      name="start-reading-session"),
    # path("books/<int:pk>/end-reading-session/", ReadingSessionViewSet.as_view({"post": "end_reading_session"}),
    #      name="end-reading-session"),
    path('start-reading-session/<int:book_id>/', StartReadingSession.as_view(), name='start-reading-session'),
    path('end-reading-session/<int:book_id>/', EndReadingSession.as_view(), name='end-reading-session'),



]

app_name = "book"
