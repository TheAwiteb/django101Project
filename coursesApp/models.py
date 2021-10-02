from django.db import models
from django.db.models.fields import PositiveSmallIntegerField
from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime
from datetime import timedelta
from pytz import UTC

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify

from django.contrib.auth.models import User

from past_date2word import past_date2word

class Courses(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, help_text="Name of the course.")
    number = PositiveSmallIntegerField(
        null=False,
        validators=[MinValueValidator(101), MaxValueValidator(10000)],
        help_text="Number of the course.",
    )
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(
        auto_now_add=True, help_text="Date of adding the course."
    )
    description = models.TextField(
        max_length=325, help_text="Description of the course.", blank=True, null=True
    )

    def is_new(self):
        return self.timestamp >= (datetime.now(tz=UTC) - timedelta(1))

    def creation_time(self):
        return past_date2word(self.timestamp)

    def description_or_nothing(self):
        return self.description or ""

    def __str__(self):
        return f"{self.name} - {self.number}"


@receiver(post_save, sender=Courses)
def make_slug(sender, instance, created, **kwargs):
    if created:
        slug = slugify(f"{instance.name} {instance.number}")
        instance.slug = slug
        instance.save()
