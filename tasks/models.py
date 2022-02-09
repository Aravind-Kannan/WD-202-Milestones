from datetime import datetime
from django.db import models

from django.contrib.auth.models import User

# For signals
from django.db.models.signals import pre_save
from django.dispatch import receiver

import pytz

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
        return self.title


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
