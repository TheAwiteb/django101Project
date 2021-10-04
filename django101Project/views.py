from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from django.contrib.auth import login, authenticate


from django.contrib import messages

from .forms import UserUpdateForm, ProfileUpdateForm, PasswordUpdateForm

get_path_name = lambda request: request.path.strip("/") or "/"


def home(request):
    path = get_path_name(request)
    context = {"path": path}
    return render(request, "home/home.html", context=context)


def about(request):
    path = get_path_name(request)
    context = {"path": path}
    return render(request, "about/about.html", context=context)


def profile(request, username):
    user = get_object_or_404(User, username=username.capitalize())
    context = {"user": user}
    return render(request, "user/user-profile.html", context=context)


def handler404(request, exception):
    response = render(
        request,
        "errors/404.html",
    )
    response.status_code = 404
    return response


class Settings(LoginRequiredMixin, TemplateView):
    template_name = "user/user-settings.html"

    def get(self, request, *args, **kwargs):
        self.user_form = UserUpdateForm(instance=request.user)
        self.profile_form = ProfileUpdateForm(instance=request.user.profile)
        self.password_form = PasswordUpdateForm()
        self.form = None
        return super(Settings, self).get(request, *args, **kwargs)

    def is_changed(self, user, instance):
        username_is_changed = user.username != instance.user.username
        email_is_changed = user.email != instance.user.email
        bio_is_changed = user.profile.bio != instance.bio
        avatar_is_changed = user.profile.avatar() != instance.avatar()
        return any(filter(lambda vlaue: type(vlaue) is bool, locals().values()))

    def post(self, request, *args, **kwargs):
        self.user_form = UserUpdateForm(request.POST, instance=request.user)
        self.password_form = PasswordUpdateForm(request.POST)
        self.form = self.request.GET.get("form")
        self.profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if self.form == "update_profile":
            if self.profile_form.is_valid() and self.user_form.is_valid():
                instance = self.profile_form.save(commit=False)
                if (
                    user := User.objects.filter(email=instance.user.email).first()
                ) and user.id != instance.user.id:
                    messages.error(request, "Email is taken.")
                else:
                    if self.is_changed(user, instance):
                        instance.save()
                        self.user_form.save()
                        messages.success(request, "Profile updated successfully.")
                    else:
                        messages.warning(request, "Nothing be changed.")
            else:
                if user_error := self.user_form.errors.get("username"):
                    messages.error(request, user_error[0])
                else:
                    messages.error(request, "Profile update unsuccessful.")
        elif self.form == "update_password":
            user = request.user
            self.password_form.user = user
            if self.password_form.is_valid():
                new_password = self.password_form.cleaned_data.get("new_password")
                user.set_password(new_password)
                user.save()
                user_authenticated = authenticate(
                    username=user.username, password=new_password
                )
                login(request, user_authenticated)
                messages.success(request, "Password changed successfully.")
            else:
                messages.error(request, "Password was not changed successfully.")
                return super(Settings, self).get(request, *args, **kwargs)
        return redirect("/settings/")

    def get_context_data(self, **kwargs):
        context = super(Settings, self).get_context_data(**kwargs)
        context.update(**kwargs)
        context["profile_forms"] = self.user_form, self.profile_form
        context["password_form"] = self.password_form
        return context
