from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),  # List all tasks
    path('create/', views.create_task, name='create_task'),  # Create a new task
    path('update/<int:task_id>/', views.update_task, name='update_task'),  # Update an existing task
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),  # Delete a task
]
