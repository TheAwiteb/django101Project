from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from django.contrib.auth import login, authenticate


from django.contrib import messages

from .forms import UserUpdateForm, ProfileUpdateForm, PasswordUpdateForm

# ارجاع المسار الخاص بالصفحة
get_path_name = lambda request: request.path.strip("/") or "/"


def home(request) -> HttpResponse:
    """عرض الصفحة الرئيسية

    المخرجات:
        HttpResponse: الصفحة الرئيسية
    """
    # جلب مسار الصفخة
    path = get_path_name(request)
    # وضع المسار في المتغيرات الخاصة بالصفحة
    context = {"path": path}
    # ارجاع الصفخة الرئيسية
    return render(request, "home/home.html", context=context)


def about(request) -> HttpResponse:
    # جلب مسار الصفحة
    path = get_path_name(request)
    # وضع المسار في المتغيرات الخاصة بالصفحة
    context = {"path": path}
    # ارجاع صفخة النبذة
    return render(request, "about/about.html", context=context)


def profile(request, username: str) -> HttpResponse:
    """عرض البروفايل الخاص باليوزر

    المعطيات:
        username (str): اسم المستخدم المراد جلب بروفايله

    الاخطاء:
        404: عدم وجود المستخدم

    المخرجات:
        HttpResponse: الصفحة الرئيسية
    """
    user = get_object_or_404(User, username=username.capitalize())
    context = {"user": user}
    return render(request, "user/user-profile.html", context=context)


def handler404(request, exception) -> HttpResponse:
    """ارجاع صفخة 404

    Returns:
        HttpResponse: صفخة 404
    """
    response = render(
        request,
        "errors/404.html",
    )
    response.status_code = 404
    return response


class Settings(LoginRequiredMixin, TemplateView):
    """اعدادات المستخدم يمكن خلالها
    1- تحديث البيانات الشخصية الخاصة بالمستخدم
    2- وتغير كلمة المرور
    3- وحذف الحساب الشخصي
    """

    # الصفخة الخاصة بالاعدادات
    template_name = "user/user-settings.html"

    def get(self, request, *args, **kwargs):
        # الفورم الخاص بتحديث البيانات الشخصية الخاصة بالمستخدم
        self.user_form = UserUpdateForm(instance=request.user)
        # الفورم الخاص بتحديث البروفايل الخاص بالمستخدم
        self.profile_form = ProfileUpdateForm(instance=request.user.profile)
        # الفورم الخاص بتغير الباسورد
        self.password_form = PasswordUpdateForm()
        # يتم حفط في هذا المتغير الفورم الذي قام المستخدم بملئه وفي هاذه الحالة لم يقوم النستخدم بملئ اي فورم
        self.form = None
        return super(Settings, self).get(request, *args, **kwargs)

    def is_changed(self, user: User, instance: User) -> bool:
        """تقوم هاذه الميثود بالمقارنة بين بيانات المستخدم قبل وبعد التغير وترجع اذا تم اجراء اي تغير عليها ام لا

        Args:
            user (User): المستخدم قبل التغير.
            instance (User): المستخدم بعد التغير.
        Returns:
            [bool]: تم اجراء تغير على بيانات المستخدم ام لا.
        """
        # المقارنة بين اسم المستخدم القديم والجديد
        username_is_changed = user.username != instance.user.username
        # المقارنة بين الايميل القديم والجديد
        email_is_changed = user.email != instance.user.email
        # المقارنة بالبايو القديم والجديد
        bio_is_changed = user.profile.bio != instance.bio
        # المقارنة بالصورة الرمزية القديمة الجديدة
        avatar_is_changed = user.profile.avatar() != instance.avatar()
        # ارجاع  صحيح ان وجد من المتغيرات المحلية المنطقية وهي التي تم تعريفها في الاعلى
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
        elif self.form == "delete_account":
            user = request.user
            user.delete()
            return redirect("/")
        return redirect("/settings/")

    def get_context_data(self, **kwargs):
        context = super(Settings, self).get_context_data(**kwargs)
        context.update(**kwargs)
        context["profile_forms"] = self.user_form, self.profile_form
        context["password_form"] = self.password_form
        return context
