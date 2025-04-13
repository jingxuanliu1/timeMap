from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Task
from .forms import TaskForm

@login_required
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'tasks/index.html', {'template_data': {'title': 'Tasks', 'tasks': []}})

    tasks = Task.objects.filter(user=request.user).order_by('start_time')
    template_data = {
        'title': 'Your Tasks',
        'tasks': tasks,
    }
    return render(request, 'tasks/index.html', {'template_data': template_data})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.latitude = form.cleaned_data.get('latitude')
            task.longitude = form.cleaned_data.get('longitude')
            task.save()
            return redirect('tasks:index')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })

@login_required
def update_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
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

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('tasks:index')

