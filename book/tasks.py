from datetime import datetime, timedelta
from celery import shared_task

from user.models import User
from book.models import ReadingSession


@shared_task
def update_reading_time_statistics():
    end_date = datetime.now()
    users = User.objects.all()

    for user in users:
        seven_days_ago = end_date - timedelta(days=7)
        relevant_sessions_7_days = ReadingSession.objects.filter(
            user=user,
            end_time__gte=seven_days_ago,
            end_time__lte=end_date,
        )
        total_reading_time_7_days = sum(
            [session.duration for session in relevant_sessions_7_days],
            timedelta(),
        )

        thirty_days_ago = end_date - timedelta(days=30)
        relevant_sessions_30_days = ReadingSession.objects.filter(
            user=user,
            end_time__gte=thirty_days_ago,
            end_time__lte=end_date,
        )
        total_reading_time_30_days = sum(
            [session.duration for session in relevant_sessions_30_days],
            timedelta(),
        )

        user.profile.total_reading_time_7_days = (
            total_reading_time_7_days / 1000000
        )
        user.profile.total_reading_time_30_days = (
            total_reading_time_30_days / 1000000
        )

        user.profile.save()
