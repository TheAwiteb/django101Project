from django import forms
from .models import Courses


class AddCourceForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = "__all__"
        labels = {"name": "", "number": ""}
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Course Name", "id":"courseName", "onkeyup":"courseNameValidator()"}
            ),
            "number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Course Number", "id":"courseNumber", "onkeyup":"courseNumebrValidator()"}
            ),
        }
        help_texts = {"name": None, "number": None}
    
    def clean_name(self, *args, **kwargs):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        if name.isdigit():
            raise forms.ValidationError(" Enter a whole course name.")
        return name
