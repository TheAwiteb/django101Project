from django.db import models
from django.db.models.fields import PositiveSmallIntegerField
from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime
from datetime import timedelta
from pytz import UTC

from django.contrib.auth.models import User


class Courses(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, help_text="Name of the course.")
    number = PositiveSmallIntegerField(
        null=False,
        validators=[MinValueValidator(101), MaxValueValidator(10000)],
        help_text="Number of the course.",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, help_text="Date of adding the course."
    )
    description = models.TextField(
        max_length=325, help_text="Description of the course.", blank=True, null=True
    )

    def is_new(self):
        return self.timestamp >= (datetime.now(tz=UTC) - timedelta(1))

    def description_or_nothing(self):
        return self.description or ''

    def __str__(self):
        return f"{self.name} - {self.number}"
