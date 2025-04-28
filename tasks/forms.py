from django import forms
from tasks.models import Task

class TaskForm(forms.ModelForm):
    NOTIFICATION_CHOICES = [
        (5, "5 minutes before"),
        (10, "10 minutes before"),
        (15, "15 minutes before"),
        (20, "20 minutes before"),
        (30, "30 minutes before"),
    ]

    notify_before = forms.ChoiceField(
        choices=NOTIFICATION_CHOICES,
        required=False,
        label="Notify me"
    )

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
        fields = [
            'title',
            'description',
            'location',
            'start_location',
            'start_time',
            'end_time',
            'completed',
            'latitude',
            'longitude',
            'latitude2',
            'longitude2',
            'notify_before',
            'recur',
            'repeat_count',
        ]
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
            }),
            'recur': forms.Select(attrs={'class': 'form-select'}),
        }

    repeat_count = forms.IntegerField(
        required=False,
        label="Repeat how many times?",
        min_value=1,
        initial=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. 5'
        })
    )


