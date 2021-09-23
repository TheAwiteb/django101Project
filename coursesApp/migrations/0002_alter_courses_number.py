# Generated by Django 3.2.7 on 2021-09-22 11:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coursesApp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courses",
            name="number",
            field=models.PositiveSmallIntegerField(
                help_text="Number of the course.",
                validators=[
                    django.core.validators.MinValueValidator(101),
                    django.core.validators.MaxValueValidator(10000),
                ],
            ),
        ),
    ]
