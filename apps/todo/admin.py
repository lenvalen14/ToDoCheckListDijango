from django.contrib import admin
from apps.todo.models import Task, SubTask, Epic

# Register your models here.
admin.site.register(Epic)
admin.site.register(Task)
admin.site.register(SubTask)

