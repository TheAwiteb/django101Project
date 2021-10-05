from django import forms
from django.contrib.auth.models import User
from registration.models import Profile

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class UserUpdateForm(forms.ModelForm):
    """
    فورم لتحديث بيانات اليوزر
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "signup_username",
                "placeholder": "Username",
                "onkeyup": "usernameValidator()",
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "signup_email",
                "placeholder": "Email",
                "onkeyup": "emailValidator()",
            }
        )
    )

    class Meta:
        model = User
        # الحقول المراد استخدامها في الفورم
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    """
    فورم لتحديث بروفايل اليوزر
    """

    class Meta:
        model = Profile
        # الحقول المراد استخدامها في الفورم
        fields = ["image", "bio"]


class PasswordUpdateForm(forms.ModelForm):
    """
    فورم لتحديث الباسورد الخاص باليوزر
    """

    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Old password",
            }
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "New password",
                "onkeyup": "passwordValidator()",
            }
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "repeat new password",
                "onkeyup": "passwordValidator()",
            }
        )
    )

    class Meta:
        model = User
        # الحقول المراد استخدامها في الفورم
        fields = []
        labels = {"new_password2": "Repeat new password"}

    def clean(self, *args, **kwargs):
        """
        دالة التحقق من معطيات الفورم

        الاخطاء:
            forms.ValidationError: اخطاء في تكوين كلمة المرور.
            forms.ValidationError: عدم تشابه كلمتي السر.
            forms.ValidationError: الباسورد القديم غير صحيح.
        """
        # لقد تم اضافة متغير اليوزر من قبل في الفيو الخاص بالاعدادات
        # ./view.py @Settings
        user = self.user
        # جلب الباسورد القديم من الفورم
        old_password = self.cleaned_data.get("old_password")
        # جلب الباسورد الجديد من الفورم
        new_password = self.cleaned_data.get("new_password")
        # جلب تكرار الباسورد الجديد من الفورم
        new_password2 = self.cleaned_data.get("new_password2")
        # اذا كان الباسورد الخاص باليوزر متطابق مع الباسورد القديم المدخل
        if user.check_password(old_password):
            # اذا كان الباسورد الجديد وتكراره متطابقين
            if new_password == new_password2:
                try:
                    # اذا كان يوجد خطأ في تكوين الباسورد سوف يتم ارجاع جميع الاخطاء
                    password_validation.validate_password(new_password, user)
                    # ارجاع الحقول المدخلة بعد التاكد من صحتها
                    return super(PasswordUpdateForm, self).clean(*args, **kwargs)
                except ValidationError as err:
                    # ارجاع جميع الاخطاء
                    raise forms.ValidationError(err.messages)
            else:
                # خطأ بعدم تطابق كلمتي المرور
                raise forms.ValidationError("The two new password fields didn’t match.")
        else:
            # خطأ بعدم صحة الباسورد القديم
            raise forms.ValidationError("The old password is incorrect.")
