from django.db import models

class Status(models.TextChoices):
    TODO = ("TODO", "TO DO")
    IN_PROGRESS = ("IN_PROGRESS", "IN PROGRESS")
    COMPLETED = ("COMPLETED", "COMPLETED")
    BLOCKED = ("BLOCKED", "BLOCKED")