from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms


class signinForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "signin_username",
                "placeholder": "Username",
                "onkeyup": "usernameValidator()",
            },
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "signin_password",
                "placeholder": "Password",
                "onkeyup": "passwordValidator()",
            }
        )
    )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        user = authenticate(username=username.capitalize(), password=password)
        if user and user.is_active:
            return super(signinForm, self).clean(*args, **kwargs)
        raise forms.ValidationError("Username or password is incorrect.")


class signupForm(UserCreationForm):
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
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "signup_password1",
                "placeholder": "Password",
                "onkeyup": "passwordValidator()",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "signup_password2",
                "placeholder": "Repeat password",
                "onkeyup": "passwordValidator()",
            }
        )
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {"username": "", "email": "", "password1": "", "password2": ""}

    def save(self, commit=True):
        user = super(signupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user

    def clean_username(self, *args, **kwargs):
        def user_is_created(username):
            return username.lower() in map(
                lambda user: user.get("username", "").lower(),
                User.objects.values("username"),
            )

        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        if len(username) >= 4:
            if user_is_created(username):
                raise forms.ValidationError("Username is already exists.")
            elif len(username) >= 20:
                raise forms.ValidationError("Username is very large.")
            elif username.isdigit() or username.isnumeric() or username.isdecimal():
                raise forms.ValidationError("Username is invalid.")
            return username.capitalize()
        else:
            raise forms.ValidationError(
                "Username is very short, it must be more than three characters."
            )

    def clean_email(self, *args, **kwargs):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        email_count = User.objects.filter(email=email).count()
        if email_count:
            raise forms.ValidationError("Email is already exists.")
        return email
