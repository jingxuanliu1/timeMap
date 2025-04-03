from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import UserProfile


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
        return user


class CustomSetPasswordForm(SetPasswordForm):
    gmail = forms.EmailField(label="Gmail Address", help_text="Please enter your Gmail address.")

    def clean_gmail(self):
        gmail = self.cleaned_data['gmail']
        if not gmail.endswith('@gmail.com'):
            raise forms.ValidationError("Please use a Gmail address (e.g., example@gmail.com).")
        if UserProfile.objects.filter(gmail=gmail).exists():
            raise forms.ValidationError("This Gmail address is already in use.")
        return gmail

    def save(self, commit=True):
        user = super().save(commit=commit)
        gmail = self.cleaned_data['gmail']
        if commit:
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'gmail': gmail}
            )
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gmail', 'phone_number', 'social_media', 'profile_image', 'bio']
        widgets = {
            'gmail': forms.TextInput(attrs={'readonly': 'readonly'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'maxlength': 500}),
        }
        labels = {
            'gmail': 'Gmail Address',
            'phone_number': 'Phone Number',
            'social_media': 'Social Media Handle',
            'profile_image': 'Profile Image',
            'bio': 'Bio',
        }
        help_texts = {
            'phone_number': 'Enter your phone number (e.g., +1234567890).',
            'social_media': 'Enter your social media handle (e.g., @username).',
            'profile_image': 'Upload your profile picture.',
            'bio': 'A short introduction about yourself (max 500 characters).',
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

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image and image.size > 5 * 1024 * 1024:  # Limit to 5MB
            raise forms.ValidationError("Image file size must be under 5MB.")
        return image

    def clean_gmail(self):
        # Since gmail is readonly, ensure it’s not changed via form tampering
        gmail = self.cleaned_data.get('gmail')
        if self.instance and self.instance.pk and gmail != self.instance.gmail:
            raise forms.ValidationError("Gmail address cannot be changed here.")
        return gmail