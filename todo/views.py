from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse

from .forms import TaskForm, TaskFormDetail
from .models import Task, SubTask, Epic


class EpicListView(ListView):
    model = Epic
    context_object_name = 'epic_list'
    template_name = 'todo/epic_list.html'

class EpicDetailView(DetailView):
    model = Epic
    template_name = 'todo/epic_detail.html'
    context_object_name = 'epic'

class EpicCreateView(CreateView):
    model = Epic
    template_name = 'todo/epic_list.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('epic-list')

class EpicUpdateView(UpdateView):
    model = Epic
    fields = ['title', 'description']
    success_url = reverse_lazy('epic-list')

class SubTaskListView(ListView):
    model = SubTask
    context_object_name = 'subtask_list'
    template_name = "todo/subtask_list.html"
    ordering = '-created_at'

class SubTaskCreateView(CreateView):
    model = SubTask
    fields = ['title', 'status']

    def form_valid(self, form):
        task = get_object_or_404(Task, pk=self.kwargs['task_pk'])
        form.instance.task = task
        return super().form_valid(form)

    def get_success_url(self):
        task_pk = self.object.task.pk
        return reverse('task-update', kwargs={'pk': task_pk})


class UpdateSubTaskStatusView(View):
    def post(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        status = request.POST.get('status')
        if status in dict(SubTask._meta.get_field('status').choices):
            subtask.status = status
            subtask.save()
        subtasks = SubTask.objects.filter(task=subtask.task)
        html = render_to_string('todo/subtask_list.html', {'subtask_list': subtasks})
        return HttpResponse(html)

class TaskListView(ListView):
    model = Task
    context_object_name = 'task_list'
    template_name = 'todo/epic_detail.html'
    ordering = '-start_day'

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        epic = get_object_or_404(Epic, pk=self.kwargs.get('epic_pk'))
        form.instance.epic = epic
        messages.success(self.request, 'Đã tạo task mới thành công!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Tạo task thất bại. Vui lòng kiểm tra lại thông tin đã nhập.')
        return redirect('epic-detail', pk=self.kwargs.get('epic_pk'))

    def get_success_url(self):
        return reverse('epic-detail', kwargs={'pk': self.object.epic.pk})

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskFormDetail
    context_object_name = 'task'
    template_name = "todo/task_detail_form.html"

    def get_success_url(self):
        return reverse('epic-detail', kwargs={'pk': self.object.epic.pk})


class DeleteSubTaskView(View):
    def delete(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        subtask.delete()
        return JsonResponse({'success': True, 'message': 'Subtask deleted'})
