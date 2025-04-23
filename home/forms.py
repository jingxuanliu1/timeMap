'''from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from profiles.models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    gmail = forms.EmailField(label="Gmail Address", help_text="Please enter your Gmail address.")

    class Meta:
        model = User
        fields = ('username', 'gmail', 'password1', 'password2')

    def clean_gmail(self):
        gmail = self.cleaned_data['gmail']
        if not gmail.endswith('@gmail.com'):
            raise forms.ValidationError("Please use a Gmail address (e.g., example@gmail.com).")
        if UserProfile.objects.filter(gmail=gmail).exists():
            raise forms.ValidationError("This Gmail address is already in use.")
        return gmail

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            UserProfile.objects.create(
                user=user,
                gmail=self.cleaned_data['gmail']
            )
        return user'''