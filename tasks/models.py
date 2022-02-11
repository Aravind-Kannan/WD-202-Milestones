import pytz
from django.contrib.auth.models import User
from django.db import models

# For signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("COMPLETED", "COMPLETED"),
    ("CANCELLED", "CANCELLED"),
)


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.IntegerField(null=False, default=0)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )

    def __str__(self):
        return f"{self.title} [Priority: {self.priority}]"


class TaskHistory(models.Model):
    old_status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    new_status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    updated_date = models.DateTimeField(auto_now=True)
    # Rethink null and blank
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)


class EmailTaskReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    send_time = models.TimeField(null=True)
    time_zone = models.CharField(max_length=32, choices=TIMEZONES, default="UTC")
    subject = models.CharField(max_length=50)
    content = models.TextField(max_length=500)
    sent = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def CreateEmailTaskReport(sender, instance, **kwargs):
    try:
        EmailTaskReport.objects.get(user=instance)
    except:
        EmailTaskReport.objects.create(
            user=instance,
            subject=instance.username + "'s report",
            content="Default Content",
        )


@receiver(post_save, sender=Task)
def UpdateEmailTaskReport(sender, instance, **kwargs):
    try:
        report = EmailTaskReport.objects.get(user=instance.user)
        all_tasks = Task.objects.filter(deleted=False, user=instance.user.id)
        content = "Task report:\n\n\n"
        for i in range(len(STATUS_CHOICES) - 1):
            tasks = all_tasks.filter(status=STATUS_CHOICES[i][0])
            content += f"{STATUS_CHOICES[i][0].title()} :  {str(tasks.count())}\n"
            for i in range(len(tasks)):
                content += f"{i + 1}. {tasks[i]}\n"
            content += "\n\n"
        report.content = content
        report.save()
        print("Updated EmailTaskReport Record!")
    except:
        print("EmailTaskReport not found!")


@receiver(pre_save, sender=Task)
def CreateTaskHistory(sender, instance, **kwargs):
    try:
        old_task = Task.objects.get(pk=instance.id)
        if old_task.status != instance.status:
            TaskHistory.objects.create(
                old_status=old_task.status, new_status=instance.status, task=instance
            ).save()
            print("Created TaskHistory Record!")
    except:
        print("Task not found!")
