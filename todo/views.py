from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.template.loader import render_to_string
from django.http import HttpResponse

from .forms import TaskForm
from .models import Task, SubTask, Epic


class EpicListView(ListView):
    model = Epic
    queryset = Epic.objects.all()
    context_object_name = 'epic_list'
    template_name = 'todo/epic_list.html'

class EpicDetailView(DetailView):
    model = Epic
    template_name = 'todo/epic_detail.html'
    context_object_name = 'epic'

class EpicCreateView(CreateView):
    model = Epic
    template_name = 'todo/epic_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('epic-list')

class EpicUpdateView(UpdateView):
    model = Epic
    template_name = 'todo/epic_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('epic-list')

class SubTaskListView(ListView):
    model = SubTask
    queryset = SubTask.objects.all()
    context_object_name = 'subtask_list'
    template_name = "todo/subtask_list.html"
    ordering = '-created_at'

class SubTaskCreateView(CreateView):
    model = SubTask
    fields = ['title', 'status']
    template_name = 'todo/subtask_form.html'

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
    queryset = Task.objects.all()
    context_object_name = 'task_list'
    template_name = 'todo/task_list.html'
    ordering = '-start_day'

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    context_object_name = 'task'
    template_name = 'todo/task_create_page.html'

    def form_valid(self, form):
        epic_pk = self.kwargs.get('epic_pk')

        epic = get_object_or_404(Epic, pk=epic_pk)

        form.instance.epic = epic

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('epic-detail', kwargs={'pk': self.object.epic.pk})

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    context_object_name = 'task'
    template_name = "todo/task_detail_form.html"

    def get_success_url(self):
        return reverse('epic-detail', kwargs={'pk': self.object.epic.pk})

class DeleteSubTaskView(View):
    def delete(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        task = subtask.task
        subtask.delete()
        subtasks = SubTask.objects.filter(task=task)
        html = render_to_string('todo/subtask_list.html', {'subtask_list': subtasks})
        return HttpResponse(html)