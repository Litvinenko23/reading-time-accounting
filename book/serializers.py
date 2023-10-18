from rest_framework import serializers

from book.models import Book, ReadingSession


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("title", "author", "publication_year", "short_description")


class BookDetailSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class ReadingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingSession
        fields = ("user", "book")
