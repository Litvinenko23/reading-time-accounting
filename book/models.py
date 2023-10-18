from datetime import timedelta

from django.db import models
from django.conf import settings


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.PositiveIntegerField()
    short_description = models.TextField()
    full_description = models.TextField()
    last_reading_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class ReadingSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reading_sessions"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reading_sessions")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    @property
    def duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        else:
            return timedelta(seconds=0)
