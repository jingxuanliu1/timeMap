from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    gmail = forms.EmailField(
        label="Gmail Address",
        help_text="Please enter your Gmail address.",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'gmail', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

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
    gmail = forms.EmailField(
        label="Gmail Address",
        help_text="Please enter your Gmail address.",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def clean_gmail(self):
        gmail = self.cleaned_data['gmail']
        if not gmail.endswith('@gmail.com'):
            raise forms.ValidationError("Please use a Gmail address (e.g., example@gmail.com).")
        if UserProfile.objects.filter(gmail=gmail).exists():
            raise forms.ValidationError("This Gmail address is already in use.")
        return gmail

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Check if UserProfile already exists before creating
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'gmail': self.cleaned_data['gmail']}
            )
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gmail', 'phone_number', 'social_media', 'profile_image', 'bio']
        widgets = {
            'gmail': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1234567890'
            }),
            'social_media': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@username'
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'maxlength': 500,
                'placeholder': 'Tell us about yourself...'
            }),
        }
        labels = {
            'gmail': 'Gmail Address',
            'phone_number': 'Phone Number',
            'social_media': 'Social Media Handle',
            'profile_image': 'Profile Image',
            'bio': 'Bio',
        }
        help_texts = {
            'phone_number': 'Must start with country code (e.g., +18035084849)',
            'social_media': 'Must start with @ (e.g., @Jliu3110)',
            'profile_image': 'Max size 5MB',
            'bio': 'Maximum 500 characters',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['gmail'].initial = self.instance.gmail

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.startswith('+'):
            raise forms.ValidationError("Phone number must start with '+' (e.g., +18035084849)")
        return phone

    def clean_social_media(self):
        social = self.cleaned_data.get('social_media')
        if social and not social.startswith('@'):
            raise forms.ValidationError("Handle must start with '@' (e.g., @Jliu3110)")
        return social

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image and image.size > 5 * 1024 * 1024:  # 5MB limit
            raise forms.ValidationError("Image size must be less than 5MB")
        return image

    def clean_gmail(self):
        gmail = self.cleaned_data.get('gmail')
        if not gmail.endswith('@gmail.com'):
            raise forms.ValidationError("Please use a Gmail address (e.g., example@gmail.com).")

        # Check if gmail is being changed and if the new one already exists
        if (self.instance and self.instance.pk and
                gmail != self.instance.gmail and
                UserProfile.objects.filter(gmail=gmail).exists()):
            raise forms.ValidationError("This Gmail address is already in use.")

        return gmail
