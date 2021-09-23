from django.db import models
from django.db.models.fields import PositiveSmallIntegerField
from django.core.validators import MaxValueValidator, MinValueValidator


class Courses(models.Model):
    name = models.CharField(max_length=100, null=False, help_text="Name of the course.")
    number = PositiveSmallIntegerField(
        null=False,
        validators=[MinValueValidator(101), MaxValueValidator(10000)],
        help_text="Number of the course.",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, help_text="Date of adding the course."
    )
