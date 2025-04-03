from django import forms
from django.contrib.auth.forms import SetPasswordForm
from .models import UserProfile

class CustomSetPasswordForm(SetPasswordForm):
    gmail = forms.EmailField(label="Gmail Address", help_text="Please enter your Gmail address.")

    def clean_gmail(self):
        gmail = self.cleaned_data['gmail']
        if not gmail.endswith('@gmail.com'):
            raise forms.ValidationError("Please use a Gmail address (e.g., example@gmail.com).")
        return gmail

    def save(self, commit=True):
        user = super().save(commit=commit)
        gmail = self.cleaned_data['gmail']
        UserProfile.objects.update_or_create(
            user=user,
            defaults={'gmail': gmail}
        )
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gmail', 'phone_number', 'social_media']
        widgets = {
            'gmail': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
        labels = {
            'gmail': 'Gmail Address',
            'phone_number': 'Phone Number',
            'social_media': 'Social Media Handle',
        }
        help_texts = {
            'phone_number': 'Enter your phone number (e.g., +1234567890).',
            'social_media': 'Enter your social media handle (e.g., @username).',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['gmail'].initial = self.instance.gmail

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.startswith('+'):
            raise forms.ValidationError("Phone number should start with '+' followed by the country code (e.g., +1234567890).")
        return phone

    def clean_social_media(self):
        social = self.cleaned_data.get('social_media')
        if social and not social.startswith('@'):
            raise forms.ValidationError("Social media handle should start with '@' (e.g., @username).")
        return social