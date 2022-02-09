# Celery - Tasks
import time
from datetime import datetime, timedelta

from celery.decorators import periodic_task
from django.core.mail import send_mail
from tasks.models import Task, User, STATUS_CHOICES, EmailTaskReport
from task_manager.celery import app


@periodic_task(run_every=timedelta(seconds=10))
def send_email_reminder():
    print("Starting to process Emails")
    for email_report in EmailTaskReport.objects.filter(
        sent=False, send_time__lte=datetime.utcnow()
    ):
        user = User.objects.get(id=email_report.user.id)
        send_mail(
            email_report.subject,
            email_report.content,
            "tasks@task_manager.org",
            [user.email],
        )
        print(f"Completed Processing User {user.id} to user email: {user.email}")
        # email_report.send = True
        email_report.save()


@app.task
def test_background_jobs():
    print("This is from the bg")
    for i in range(10):
        time.sleep(1)
        print(i)
