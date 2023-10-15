from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("title", "author", "publication_year", "short_description")


class BookDetailSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = "__all__"
