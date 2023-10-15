from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from book.models import Book, ReadingSession
from book.serializers import BookDetailSerializer, BookSerializer, ReadingSessionSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BookDetailSerializer
        return BookSerializer


class ReadingSessionViewSet(viewsets.ModelViewSet):
    queryset = ReadingSession.objects.all()
    serializer_class = ReadingSessionSerializer

    @action(detail=True, methods=["post"])
    def start_reading_session(self, request, pk=None):
        book = self.get_object()
        user = request.user

        book_id = int(request.data.get("book_id"))

        existing_session = ReadingSession.objects.filter(
            user=user,
            book_id=book_id,
            end_time__isnull=True).first()

        if existing_session:
            return Response({"error": "Session with this book already started."}, status=status.HTTP_400_BAD_REQUEST)

        new_session = ReadingSession.objects.create(user=user, book=book)

        return Response({"message": "Reading session started successfully."}, status=status.HTTP_200_OK)

    def end_reading_session(self, request, pk=None):
        book = self.get_object()
        user = request.user

        book_id = int(request.data.get("book_id"))

        session = ReadingSession.objects.filter(
            user=user,
            book_id=book_id,
            end_time__isnull=True).first()
        if not session:
            return Response({"error": "No active reading session with this book."}, status=status.HTTP_400_BAD_REQUEST)

        session.end_time = timezone.now()
        session.save()

        return Response({"message": "Reading session ended successfully."}, status=status.HTTP_200_OK)


