from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from django.contrib import messages

from .forms import UserUpdateForm, ProfileUpdateForm

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
    user = User.objects.filter(username=username.capitalize()).first()
    context = {"user": user}
    if user:
        return render(request, "user/user-profile.html", context=context)
    else:
        raise Http404


def handler404(request, exception):
    response = render(
        request,
        "errors/404.html",
    )
    response.status_code = 404
    return response


class Settings(LoginRequiredMixin, TemplateView):
    template_name = "user/user-settings.html"

    def get(self, request):
        self.user_form = UserUpdateForm(instance=request.user)
        self.profile_form = ProfileUpdateForm(instance=request.user.profile)
        return super().render_to_response(self.get_context_data())

    def is_changed(self, user, instance):
        username_is_changed = user.username != instance.user.username
        email_is_changed = user.email != instance.user.email
        bio_is_changed = user.profile.bio != instance.bio
        avatar_is_changed = user.profile.avatar() != instance.avatar()
        print(locals().values())
        return any(filter(lambda vlaue: type(vlaue) is bool, locals().values()))

    def post(self, request):
        self.user_form = UserUpdateForm(request.POST, instance=request.user)
        self.profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

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
            if self.user_form.errors.get("username"):
                messages.error(request, "Username is taken.")
            else:
                messages.error(request, "Profile update unsuccessful.")
        return redirect("/settings/")

    def get_context_data(self, **kwargs):
        context = super(Settings, self).get_context_data(**kwargs)
        context.update(**kwargs)
        context["forms"] = self.user_form, self.profile_form
        return context
