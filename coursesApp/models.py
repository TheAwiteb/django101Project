from django.db import models
from django.db.models.fields import PositiveSmallIntegerField


class Courses(models.Model):
    name = models.CharField(max_length=100, null=False, help_text="Name of the course.")
    number = PositiveSmallIntegerField(null=False, help_text="Number of the course.")
    timestamp = models.DateTimeField(
        auto_now_add=True, help_text="Date of adding the course."
    )
