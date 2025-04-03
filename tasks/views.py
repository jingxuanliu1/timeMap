from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

# View to display all tasks
@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user).order_by('start_time')  # Get tasks for the logged-in user
    return render(request, 'tasks/index.html', {'tasks': tasks})

# View to create a new task
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        print('first one')
        if form.is_valid():
            print('second one')
            task = form.save(commit=False)
            task.user = request.user  # Assign the task to the current user
            task.save()
            return redirect('tasks:index')  # Redirect to the task list
        else: print('I RAN',form.errors)
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})

# View to update an existing task
@login_required
def update_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:index')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/update_task.html', {'form': form, 'task': task})

# View to delete a task
@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('tasks:index')


