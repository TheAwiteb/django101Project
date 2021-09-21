from django.shortcuts import render
from .models import Courses


get_path_name = lambda request: request.path.strip("/")


def coursesList(request):
    courses = list(
        map(
            lambda dct: {
                key: val.title() if key == "name" else val for key, val in dct.items()
            },
            Courses.objects.all().values(),
        )
    )
    path = get_path_name(request)
    context = {"path": path, "courses": courses, "courses_count": len(courses)}
    return render(request, "coursesApp/courses-home.html", context=context)
