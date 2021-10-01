from django import forms
from django.contrib.auth.models import User
from registration.models import Profile

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


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


class PasswordUpdateForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Old password",
            }
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "New password",
                "onkeyup": "passwordValidator()",
            }
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "repeat new password",
                "onkeyup": "passwordValidator()",
            }
        )
    )

    class Meta:
        model = User
        fields = []
        labels = {"new_password2":"repeat new password"}

    def clean(self, *args, **kwargs):
        user = self.user
        old_password = self.cleaned_data.get("old_password")
        new_password = self.cleaned_data.get("new_password")
        new_password2 = self.cleaned_data.get("new_password2")
        if user.check_password(old_password):
            if new_password == new_password2:
                try:
                    # If the password is valid, return None. If the password is invalid, raise ValidationError with all error messages.
                    password_validation.validate_password(new_password, user)
                    return super(PasswordUpdateForm, self).clean(*args, **kwargs)
                except ValidationError as err:
                    raise forms.ValidationError(err.messages)
            else:
                raise forms.ValidationError("The two new password fields didn’t match.")
        else:
            raise forms.ValidationError("The old password is incorrect.")
