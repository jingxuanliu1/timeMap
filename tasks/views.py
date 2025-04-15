from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Task
from .forms import TaskForm

# View to display all tasks
@login_required
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'tasks/index.html', {'template_data': {'title': 'Tasks', 'tasks': []}})
    tasks = Task.objects.filter(user=request.user).order_by('start_time')  # Get tasks for the logged-in user
    completed_count = Task.objects.filter(user=request.user).filter(completed=True).count()
    return render(request, 'tasks/index.html', {'tasks': tasks, 'completed_count': completed_count})

# View to create a new task
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the task to the current user
            # Explicitly set latitude and longitude from form data
            task.latitude = form.cleaned_data.get('latitude')
            task.longitude = form.cleaned_data.get('longitude')
            task.save()
            return redirect('tasks:index')  # Redirect to the task list
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })

# View to update an existing task
@login_required
def update_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            # Explicitly set latitude and longitude from form data
            task.latitude = form.cleaned_data.get('latitude')
            task.longitude = form.cleaned_data.get('longitude')
            task.save()
            return redirect('tasks:index')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/update_task.html', {
        'form': form,
        'task': task,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })

# View to delete a task
@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('tasks:index')


