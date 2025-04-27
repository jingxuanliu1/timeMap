from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
<<<<<<< HEAD
    email = forms.EmailField(
        label="Email Address",
        help_text="Please enter your email address.",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
=======
    email = forms.EmailField(required=True)  # Make sure this is here
>>>>>>> main

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

<<<<<<< HEAD
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
=======
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
>>>>>>> main
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
<<<<<<< HEAD
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            UserProfile.objects.get_or_create(user=user, defaults={'email': self.cleaned_data['email']})
=======
        user.email = self.cleaned_data['email']  # Ensure email is saved
        if commit:
            user.save()
            # Remove the profile creation here since the signal handles it
>>>>>>> main
        return user


class CustomSetPasswordForm(SetPasswordForm):
<<<<<<< HEAD
    email = forms.EmailField(
        label="Email Address",
        help_text="Please enter your email address.",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

=======
>>>>>>> main
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
<<<<<<< HEAD
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'email': self.cleaned_data['email']}
            )
=======
            UserProfile.objects.get_or_create(user=user)
>>>>>>> main
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
<<<<<<< HEAD
        fields = ['phone_number', 'social_media', 'profile_image', 'bio']  # ← email 제거
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
=======
        fields = ['phone_number', 'social_media', 'profile_image', 'bio']
        widgets = {
>>>>>>> main
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
<<<<<<< HEAD
            'email': 'Email Address',
=======
>>>>>>> main
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

<<<<<<< HEAD
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['email'].initial = self.instance.email

=======
>>>>>>> main
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
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image size must be less than 5MB")
        return image
<<<<<<< HEAD

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if (self.instance and self.instance.pk and
                email != self.instance.email and
                UserProfile.objects.filter(email=email).exists()):
            raise forms.ValidationError("This email address is already in use.")
        return email
=======
>>>>>>> main
