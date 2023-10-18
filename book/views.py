from datetime import timedelta

from django.db.models import Sum, ExpressionWrapper, fields, F
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book, ReadingSession
from book.serializers import (
    BookDetailSerializer,
    BookSerializer,
    ReadingSessionSerializer,
    BookListSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer

        if self.action == "retrieve":
            return BookDetailSerializer

        return BookSerializer


class ReadingSessionViewSet(viewsets.ModelViewSet):
    queryset = ReadingSession.objects.all()
    serializer_class = ReadingSessionSerializer


class StartReadingSession(APIView):
    def post(self, request, book_id):
        # Check if the user is authenticated and get the user instance
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if there's an active reading session for this book
        active_sessions = ReadingSession.objects.filter(
            book=book, end_time__isnull=True
        )
        if active_sessions.exists():
            return Response(
                {
                    "detail": "An active reading session for this book already exists."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Find and end the previous session if one exists
        try:
            previous_session = ReadingSession.objects.get(
                user=request.user, end_time__isnull=True
            )
            previous_session.end_time = timezone.now()
            previous_session.save()
        except ReadingSession.DoesNotExist:
            pass  # No active session to end

        # Create a new reading session
        reading_session = ReadingSession(
            user=request.user, book=book, start_time=timezone.now()
        )
        reading_session.save()

        book.last_reading_date = reading_session.start_time
        book.save()

        return Response(
            {"detail": "Reading session started"},
            status=status.HTTP_201_CREATED,
        )


class EndReadingSession(APIView):
    def post(self, request, book_id):
        # Check if the user is authenticated and get the user instance
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            reading_session = ReadingSession.objects.get(
                user=request.user, book=book, end_time__isnull=True
            )
            reading_session.end_time = timezone.now()
            reading_session.save()
            return Response(
                {"detail": "Reading session ended"}, status=status.HTTP_200_OK
            )
        except ReadingSession.DoesNotExist:
            return Response(
                {"detail": "No active reading session found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class TotalReadingTime(APIView):
    def get(self, request, book_id):
        total_reading_time = ReadingSession.objects.filter(
            book_id=book_id
        ).aggregate(
            total=Sum(
                ExpressionWrapper(
                    F("end_time") - F("start_time"),
                    output_field=fields.DurationField(),
                )
            )
        )

        return Response({"total_reading_time": total_reading_time["total"]})


class UserStatistics(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user  # Get the currently authenticated user
            reading_sessions = ReadingSession.objects.filter(user=user)

            # Calculate total_reading_time for the user
            total_duration = sum(
                (session.duration for session in reading_sessions), timedelta()
            )

            return Response({"total_reading_time_hours": total_duration})
        else:
            return Response(
                {"detail": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
