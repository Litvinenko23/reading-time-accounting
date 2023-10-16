from django.urls import path, include
from rest_framework.routers import DefaultRouter

from book.views import BookViewSet, ReadingSessionViewSet, StartReadingSession, EndReadingSession, TotalReadingTime, UserStatistics


router = DefaultRouter()
router.register("books", BookViewSet)
router.register("reading-sessions", ReadingSessionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("start-reading-session/<int:book_id>/", StartReadingSession.as_view(), name="start-reading-session"),
    path("end-reading-session/<int:book_id>/", EndReadingSession.as_view(), name="end-reading-session"),
    path("total-reading-time/<int:book_id>/", TotalReadingTime.as_view(), name="total-reading-time"),
    path('user-statistics/', UserStatistics.as_view(), name='user-statistics'),
]

app_name = "book"
