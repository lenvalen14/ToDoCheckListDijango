from django.shortcuts import render, get_object_or_404
from .models import Task, SubTask

# --- Views cho Task chính ---
def task_list(request):
    tasks = Task.objects.order_by('completed', '-id')
    return render(request, 'todo/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
    tasks = Task.objects.order_by('completed', '-id')
    return render(request, 'todo/task_list_partial.html', {'tasks': tasks})

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    new_status = not task.completed
    task.completed = new_status
    task.save()
    task.subtasks.update(completed=new_status)
    tasks = Task.objects.order_by('completed', '-id')
    return render(request, 'todo/task_list_partial.html', {'tasks': tasks})

def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()
    tasks = Task.objects.order_by('completed', '-id')
    return render(request, 'todo/task_list_partial.html', {'tasks': tasks})

# --- Views cho SubTask ---
def get_subtasks(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'todo/subtask_list.html', {'subtasks': task.subtasks.all(), 'parent_task': task})

def add_subtask(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            SubTask.objects.create(title=title, task=task)
    return render(request, 'todo/subtask_list.html', {'subtasks': task.subtasks.all(), 'parent_task': task})

def complete_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)
    subtask.completed = not subtask.completed
    subtask.save()
    task = subtask.task
    if task.all_subtasks_completed():
        task.completed = True
    else:
        task.completed = False
    task.save()
    all_tasks = Task.objects.order_by('completed', '-id')
    context = {
        'subtasks': task.subtasks.all(),
        'parent_task': task,
        'tasks': all_tasks
    }
    return render(request, 'todo/partials/subtask_update_response.html', context)

def delete_subtask(request, subtask_id):
    if request.method == 'POST':
        subtask = get_object_or_404(SubTask, id=subtask_id)
        task = subtask.task
        subtask.delete()
        return render(request, 'todo/subtask_list.html', {'subtasks': task.subtasks.all(), 'parent_task': task})