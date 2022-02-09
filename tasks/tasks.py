# Celery - Tasks
import time
from datetime import datetime, timedelta

from celery.decorators import periodic_task

from django.core.mail import send_mail
from pytz import timezone
from task_manager.celery import app

from tasks.models import STATUS_CHOICES, EmailTaskReport, Task, User


@periodic_task(run_every=timedelta(seconds=10))
def send_email_reminder():
    print("Starting to process Emails")
    now_utc = datetime.now(timezone("UTC"))
    for e in EmailTaskReport.objects.all():
        print(e.user, e.sent)
    for email_report in EmailTaskReport.objects.filter(sent=False):
        if (
            email_report.send_time
            <= now_utc.astimezone(timezone(email_report.time_zone)).time()
        ):
            user = User.objects.get(id=email_report.user.id)
            send_mail(
                email_report.subject,
                email_report.content,
                "tasks@task_manager.org",
                [user.email],
            )
            email_report.sent = True
            email_report.save()
            print("Email sent!")
            print(f"Completed Processing User {user.id} to user email: {user.email}")
        else:
            print("Email NOT sent!")
        print(
            email_report.send_time,
            now_utc.astimezone(timezone(email_report.time_zone)).time(),
        )


@app.task
def reset_email_sent():
    EmailTaskReport.objects.all().update(sent=False)
    print("Reset all email sent field!")
