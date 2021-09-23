from django.views.generic.list import ListView
from .models import Courses
from .forms import AddCourceForm

get_path_name = lambda request: request.path.strip("/")


class CoursesListView(ListView):
    template_name = "coursesApp/courses-home.html"
    context_object_name = "courses"
    model = Courses
    paginate_by = 7

    def get_queryset(self):
        courses = list(
            map(
                lambda dct: {
                    key: val.title() if key == "name" else val
                    for key, val in dct.items()
                },
                Courses.objects.all().order_by("-timestamp").values(),
            )
        )
        self.courses_count = len(courses)
        return courses

    def get(self, request, *args, **kwargs):
        self.add_cource_form = AddCourceForm(
            data=request.GET, use_required_attribute=False
        )
        return super(CoursesListView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.add_cource_form = AddCourceForm(
            data=request.POST, use_required_attribute=False
        )
        if self.add_cource_form.is_valid():
            self.add_cource_form.save()
        return super(CoursesListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CoursesListView, self).get_context_data(**kwargs)
        context.update(**kwargs)
        context["path"] = get_path_name(self.request)
        context["add_cource_form"] = AddCourceForm(
            data=self.request.POST or None, use_required_attribute=False
        )
        context["courses_count"] = self.courses_count
        return context
