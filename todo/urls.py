from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),

    path('task/<int:task_id>/subtasks/', views.get_subtasks, name='get_subtasks'),
    path('task/<int:task_id>/add-subtask/', views.add_subtask, name='add_subtask'),
    path('subtask/complete/<int:subtask_id>/', views.complete_subtask, name='complete_subtask'),
    path('subtask/delete/<int:subtask_id>/', views.delete_subtask, name='delete_subtask'),
]