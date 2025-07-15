from django.contrib import admin
from todo.models import Task, SubTask

# Register your models here.
admin.site.register(Task)
admin.site.register(SubTask)

