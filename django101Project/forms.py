from django import forms
from django.contrib.auth.models import User
from registration.models import Profile


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "signup_username",
                "placeholder": "Username",
                "onkeyup": "usernameValidator()",
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "signup_email",
                "placeholder": "Email",
                "onkeyup": "emailValidator()",
            }
        )
    )

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "bio"]
