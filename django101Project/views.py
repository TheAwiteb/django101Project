from django.shortcuts import render

get_path_name = lambda request: request.path.strip("/") or "/"

def home(request):
    path = get_path_name(request)
    context = {"path": path}
    return render(request, "home/home.html", context=context)


def about(request):
    path = get_path_name(request)
    context = {"path": path}
    return render(request, "about/about.html", context=context)
