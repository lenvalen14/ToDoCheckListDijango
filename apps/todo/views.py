"""
Django views for managing Epics, Tasks, and Subtasks in the ToDo application.
This module provides views for listing, creating, updating, and detailing Epics,
Tasks, and Subtasks, including AJAX functionalities for status updates and deletions.
"""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse

from .forms import TaskForm, TaskFormDetail
from .models import Task, SubTask, Epic


class EpicListView(ListView):
    """
    Displays a list of all Epics.
    """
    model = Epic
    context_object_name = 'epic_list'
    template_name = 'todo/epic_list.html'

class EpicDetailView(DetailView):
    """
    Displays the details of a single Epic, including its associated Tasks.
    """
    model = Epic
    template_name = 'todo/epic_detail.html'
    context_object_name = 'epic'

class EpicCreateView(CreateView):
    """
    Handles the creation of a new Epic.
    """
    model = Epic
    template_name = 'todo/epic_list.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('epic-list')

class EpicUpdateView(UpdateView):
    """
    Handles the updating of an existing Epic.
    """
    model = Epic
    fields = ['title', 'description']
    success_url = reverse_lazy('epic-list')

class SubTaskListView(ListView):
    """
    Displays a list of SubTasks.
    """
    model = SubTask
    context_object_name = 'subtask_list'
    template_name = "todo/subtask_list.html"
    ordering = '-created_at'

class SubTaskCreateView(CreateView):
    """
    Handles the creation of a new SubTask associated with a specific Task.
    """
    model = SubTask
    fields = ['title', 'status']

    def form_valid(self, form):
        """
        Sets the associated Task for the new SubTask before saving.
        """
        task = get_object_or_404(Task, pk=self.kwargs['task_pk'])
        form.instance.task = task
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirects to the Task detail/update page after successful SubTask creation.
        """
        task_pk = self.object.task.pk
        return reverse('task-update', kwargs={'pk': task_pk})


class UpdateSubTaskStatusView(View):
    """
    Handles updating the status of a SubTask via an AJAX POST request.
    It returns the updated list of subtasks as HTML.
    """
    def post(self, request, pk):
        """
        Updates the subtask's status based on POST data.
        Returns an HTML snippet of the updated subtask list for the associated task.
        """
        subtask = get_object_or_404(SubTask, pk=pk)
        status = request.POST.get('status')

        # Use the recommended way to access field choices
        if status in dict(subtask.status.field.choices):
            subtask.status = status
            subtask.save()

        # Fetch all subtasks related to the parent task
        subtasks = SubTask.objects.filter(task=subtask.task).order_by('-created_at')
        html = render_to_string('todo/subtask_list.html', {'subtask_list': subtasks})
        return HttpResponse(html)

class TaskListView(ListView):
    """
    Displays a list of Tasks. This view is typically used within an Epic's detail page.
    """
    model = Task
    context_object_name = 'task_list'
    template_name = 'todo/epic_detail.html'
    ordering = '-start_day'

class TaskCreateView(CreateView):
    """
    Handles the creation of a new Task associated with a specific Epic.
    """
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        """
        Associates the new Task with an Epic and saves it.
        Displays a success message.
        """
        epic = get_object_or_404(Epic, pk=self.kwargs.get('epic_pk'))
        form.instance.epic = epic
        messages.success(self.request, 'Đã tạo task mới thành công!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handles invalid form submission for Task creation.
        Displays an error message and redirects back to the Epic detail page.
        """
        messages.error(self.request, 'Tạo task thất bại. Vui lòng kiểm tra lại thông tin đã nhập.')
        return redirect('epic-detail', pk=self.kwargs.get('epic_pk'))

    def get_success_url(self):
        """
        Redirects to the Epic detail page after successful Task creation.
        """
        return reverse('epic-detail', kwargs={'pk': self.object.epic.pk})

class TaskUpdateView(UpdateView):
    """
    Handles the updating of an existing Task.
    """
    model = Task
    form_class = TaskFormDetail
    context_object_name = 'task'
    template_name = "todo/task_detail_form.html"

    def get_success_url(self):
        """
        Redirects to the Epic detail page after successful Task update.
        """
        return reverse('epic-detail', kwargs={'pk': self.object.epic.pk})


class DeleteSubTaskView(View):
    """
    Handles the deletion of a SubTask via an AJAX DELETE request.
    """
    def delete(self, request, pk):
        """
        Deletes it a SubTask instance.
        Returns a JSON response indicating success or failure.
        """
        try:
            subtask = get_object_or_404(SubTask, pk=pk)
            subtask.delete()
            return JsonResponse({'success': True, 'message': 'Subtask deleted successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error deleting subtask: {e}'}, status=400)