from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404

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

    user = User.objects.filter(username=username).first()
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
