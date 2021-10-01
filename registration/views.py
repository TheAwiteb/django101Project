from django.shortcuts import redirect

from django.contrib import messages

from django.contrib.auth import login, logout, authenticate

from django.views.generic.base import TemplateView
from .forms import signinForm, signupForm


class Registration(TemplateView):
    template_name = "registration.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            self.signin_form = signinForm(use_required_attribute=False)
            self.signup_form = signupForm(use_required_attribute=False)
            self.form = None
            return super(Registration, self).get(request, *args, **kwargs)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            self.signin_form = signinForm(request.POST, use_required_attribute=False)
            self.signup_form = signupForm(request.POST, use_required_attribute=False)
            self.form = self.request.GET.get("form")

            if self.form == "signup":
                if self.signup_form.is_valid():
                    self.signup_form.save()
                    username = self.signup_form.cleaned_data.get("username")
                    messages.success(
                        request,
                        f"Account created successfully for {username}, Please sign in",
                    )
                else:
                    messages.error(request, "Sign Up unsuccessful")
                return super(Registration, self).get(request, *args, **kwargs)

            elif self.form == "signin":
                attempts = request.session.get("attempts", 0)
                if attempts <= 15:
                    if self.signin_form.is_valid():
                        username = self.signin_form.cleaned_data.get("username")
                        password = self.signin_form.cleaned_data.get("password")
                        user = authenticate(
                            username=username.capitalize(), password=password
                        )
                        login(request, user)
                        messages.success(request, "You are logged in successfully.")
                        return redirect("/")
                    request.session["attempts"] = attempts + 1
                    messages.error(request, "Sign In unsuccessful.")
                else:
                    messages.error(
                        request, "Sorry, you have crossed your allowed attempts."
                    )
                return redirect("/registration/")
        return redirect("/")

    def get_context_data(self, **kwargs):
        context = super(Registration, self).get_context_data(**kwargs)
        context.update(**kwargs)
        context["signin_form"] = self.signin_form
        context["signup_form"] = self.signup_form
        context["form"] = self.form
        return context


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")
