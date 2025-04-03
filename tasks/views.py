from django.shortcuts import render
from .models import Task

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'tasks/index.html', {'template_data': {'title': 'Tasks', 'tasks': []}})

    # Fetch tasks for the logged-in user
    tasks = Task.objects.filter(user=request.user)
    template_data = {
        'title': 'Your Tasks',
        'tasks': tasks,
    }
    return render(request, 'tasks/index.html', {'template_data': template_data})