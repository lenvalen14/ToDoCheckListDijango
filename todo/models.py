from typing import Any

from django.utils import timezone

from django.db import models
from todo.enum import Status

# Create your models here.
class Epic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.title

    def get_task_progress(self):
        tasks = self.tasks.all()
        if not tasks.exists():
            return 0
        completed_tasks = tasks.filter(status='COMPLETED').count()
        return int((completed_tasks / tasks.count()) * 100)

class Task(models.Model):
    title = models.CharField(max_length=200)
    start_day = models.DateField(default=timezone.now)
    duration = models.IntegerField(default=0)
    status = models.CharField(max_length=12,
                              choices=Status.choices,
                              default=Status.TODO
                              )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    epic = models.ForeignKey(Epic, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    def __str__(self):
        return self.title

    @property
    def is_completed(self):
        return self.status == self.Status.COMPLETED

    def all_subtasks_completed(self):
        return not self.subtasks.filter(is_completed=False).exists()

    def get_subtask_progress_display(self):
        total = self.subtasks.count()
        completed = self.subtasks.filter(status='COMPLETED').count()
        return f"{completed}/{total}"

    @is_completed.setter
    def is_completed(self, value):
        self._is_completed = value


class SubTask(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=12,
                              choices=Status.choices,
                              default=Status.TODO
                              )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')

    def __str__(self):
        return self.title

    @property
    def is_completed(self):
        return self.status == self.Status.COMPLETED