# Generated by Django 3.2.7 on 2021-09-28 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registration", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="bio",
            field=models.TextField(blank=True, help_text="Your bio", null=True),
        ),
    ]
