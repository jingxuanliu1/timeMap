from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'location', 'start_time', 'end_time', 'completed', 'travel_time']
