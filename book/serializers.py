from rest_framework import serializers

from book.models import Book, ReadingSession


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # fields = ("title", "author", "publication_year", "short_description", "full_description")
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


# class BookReadingTimeSerializer(serializers.Serializer):
#     book_id = serializers.IntegerField(source="book__id")
#     book_title = serializers.CharField(source="book__title")
#     total_reading_time = serializers.DurationField()
#
#
# class UserStatisticsSerializer(serializers.Serializer):
#     user_id = serializers.IntegerField()
#     total_reading_time = serializers.DurationField()
