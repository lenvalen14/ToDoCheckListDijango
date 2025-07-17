from django.urls import path
from .views import (
    EpicListView,
    EpicCreateView,
    EpicUpdateView,
    TaskListView,
    SubTaskListView,
    TaskCreateView,
    TaskUpdateView, EpicDetailView, SubTaskCreateView, UpdateSubTaskStatusView, DeleteSubTaskView
)

urlpatterns = [
    path('', EpicListView.as_view(), name='epic-list'),
    path('epic/add/', EpicCreateView.as_view(), name='epic-create'),
    path('epic/<int:pk>/', EpicDetailView.as_view(), name='epic-detail'),
    path('epic/<int:pk>/update/', EpicUpdateView.as_view(), name='epic-update'),
    path('tasks/', TaskListView.as_view(), name='task-list-all'),
    path('epic/<int:epic_pk>/task/add/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/task/<int:pk>/', TaskUpdateView.as_view(), name='task-detail'),
    path('task/<int:task_pk>/subtask/add/', SubTaskCreateView.as_view(), name='subtask-create'),
    path('task/<int:task_pk>/subtasks/', SubTaskListView.as_view(), name='subtask-list'),
    path('subtask/<int:pk>/update-status/', UpdateSubTaskStatusView.as_view(), name='update_subtask_status'),
    path('subtask/<int:pk>/delete/', DeleteSubTaskView.as_view(), name='delete_subtask')
]