# Celery - Tasks
from datetime import timedelta
import time
from datetime import datetime, timedelta

from celery.decorators import periodic_task
from django.core.mail import send_mail
from pytz import timezone
from task_manager.celery import app

from tasks.models import STATUS_CHOICES, EmailTaskReport, Task, User


@periodic_task(run_every=timedelta(seconds=300))
def send_email_reminder():
    print("Starting to process Emails")
    now_utc = datetime.now(timezone("UTC"))

    for email_report in EmailTaskReport.objects.filter(send_time__lt=now_utc):
        user = User.objects.get(id=email_report.user.id)
        send_mail(
            email_report.subject,
            email_report.content,
            "tasks@task_manager.org",
            [user.email],
        )
        email_report.send_time = email_report.send_time + timedelta(days=1)
        email_report.save()
        print("Email sent!")
        print(f"Completed Processing User {user.id} to user email: {user.email}")
