from django.shortcuts import render


def home(request):
    path = "/"
    context = {"path": path}
    return render(request, "home/home.html", context=context)


def about(request):
    path = "About"
    context = {"path": path}
    return render(request, "about/about.html", context=context)
