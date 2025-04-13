# tasks/forms.py - Updated version
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    due_date = forms.DateTimeField(  # Add this
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        required=False
    )
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Task
        widgets = {
            'location': forms.TextInput(attrs={
                'id': 'location-input',
                'class': 'form-control',
                'placeholder': 'Enter location'
            }),
            'priority': forms.NumberInput(attrs={
                'min': 1,
                'max': 5
            })
        }
        fields = ['title', 'description', 'location', 'start_time', 'end_time',
                 'due_date', 'priority', 'completed', 'latitude', 'longitude']

