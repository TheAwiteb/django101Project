from django.shortcuts import render, redirect
from .models import Courses
from .forms import AddCourceForm

get_path_name = lambda request: request.path + "/"


def coursesList(request):
    courses = list(
        map(
            lambda dct: {
                key: val.title() if key == "name" else val for key, val in dct.items()
            },
            Courses.objects.all().values(),
        )
    )
    add_cource_form = AddCourceForm(data=request.POST or None, use_required_attribute=False)
    path = get_path_name(request)
    context = {
        "path": path,
        "courses": courses,
        "add_cource_form": add_cource_form,
    }
    if add_cource_form.is_valid():
        add_cource_form.save()
        return redirect("/Courses-list/", context=context)
    return render(request, "coursesApp/courses-home.html", context=context)
