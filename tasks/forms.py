from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    latitude2 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude2 = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Task
        widgets = {
            'location': forms.TextInput(attrs={
                'id': 'location-input',
                'class': 'form-control',
                'placeholder': 'Enter End location'
            }),
            'start_location': forms.TextInput(attrs={
                'id': 'location-input2',
                'class': 'form-control',
                'placeholder': 'Enter Start location'
            })
        }
        fields = ['title', 'description', 'location', 'start_location',
                 'start_time', 'end_time', 'completed',
                 'latitude', 'longitude', 'latitude2', 'longitude2']