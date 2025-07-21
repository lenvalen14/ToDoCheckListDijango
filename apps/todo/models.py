"""
Defines the data models for the ToDo application, including Epics, Tasks, and SubTasks.
These models represent the structure of the task management system.
"""

from django.utils import timezone
from django.db import models
from apps.todo.enum import Status # Assuming Status is correctly defined and imported

# Create your models here.
class Epic(models.Model):
    """
    Represents a major project or theme, containing multiple tasks.
    """
    title = models.CharField(max_length=200, verbose_name="Tiêu đề Epic")
    description = models.TextField(verbose_name="Mô tả Epic")

    class Meta:
        verbose_name = "Epic"
        verbose_name_plural = "Epics"

    def __str__(self):
        """
        Returns the title of the Epic.
        """
        return self.title

    def get_task_progress(self) -> int:
        """
        Calculates the completion progress of tasks within this Epic.
        Returns the percentage of completed tasks (0-100).
        """
        tasks = self.tasks.all()
        if not tasks.exists():
            return 0
        completed_tasks = tasks.filter(status=Status.COMPLETED).count()
        return int((completed_tasks / tasks.count()) * 100)

class Task(models.Model):
    """
    Represents an individual task, belonging to an Epic and possibly containing subtasks.
    """
    title = models.CharField(max_length=200, verbose_name="Tiêu đề Task")
    start_day = models.DateField(default=timezone.now, verbose_name="Ngày bắt đầu")
    duration = models.IntegerField(default=0, verbose_name="Thời lượng (ngày)")
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.TODO,
        verbose_name="Trạng thái Task"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    epic = models.ForeignKey(Epic, on_delete=models.CASCADE, related_name='tasks', verbose_name="Epic liên quan")

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['start_day', 'title'] # Optional: Add default ordering

    def __str__(self):
        """
        Returns the title of the Task.
        """
        return self.title

    @property
    def is_completed(self) -> bool:
        """
        Checks if the task's status is 'COMPLETED'.
        """
        # Pylint E1101: Instance of 'Task' has no 'Status' member; maybe 'status'?
        # Corrected: Access Status directly from the imported enum.
        return self.status == Status.COMPLETED

    def all_subtasks_completed(self) -> bool:
        """
        Checks if all associated subtasks are completed.
        Returns True if no subtasks exist or all existing subtasks are completed.
        """
        # Pylint E1101: Instance of 'Task' has no 'subtasks' member - False positive
        # due to Django's related_name.
        return not self.subtasks.filter(status=Status.TODO).exists()

    def get_subtask_progress_display(self) -> str:
        """
        Returns a string representing the progress of subtasks (e.g., "3/5").
        """
        # Pylint E1101: Instance of 'Task' has no 'subtasks' member - False positive
        total = self.subtasks.count()
        completed = self.subtasks.filter(status=Status.COMPLETED).count()
        return f"{completed}/{total}"

    # Removed the @is_completed.setter as it was not correctly updating the model field.
    # To change status, directly update self.status = Status.COMPLETED and save().


class SubTask(models.Model):
    """
    Represents a smaller, actionable item within a Task.
    """
    title = models.CharField(max_length=200, verbose_name="Tiêu đề SubTask")
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.TODO,
        verbose_name="Trạng thái SubTask"
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks', verbose_name="Task liên quan")

    class Meta:
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"
        ordering = ['title'] # Optional: Add default ordering

    def __str__(self):
        """
        Returns the title of the SubTask.
        """
        return self.title

    @property
    def is_completed(self) -> bool:
        """
        Checks if the subtask's status is 'COMPLETED'.
        """
        return self.status == Status.COMPLETED