from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from PIL import Image

from string import ascii_letters, digits
from random import choice

from django.conf import settings
import os
from shutil import rmtree

default_avatar_url = "https://avatars.dicebear.com/api/initials/:{username}.svg"
random_string = lambda: ''.join(choice(ascii_letters+digits) for _ in range(22))

def user_avatar_directory_path(instance, _=None):
    avatar_name = f"users/avatars/{instance.user.id}/{random_string()}.png"
    dir_path = os.path.join(settings.MEDIA_ROOT, 'users', 'avatars', str(instance.user.id))

    # django doesn't write on the image so we have to delete it manually before giving it a name
    if os.path.exists(dir_path):
        rmtree(dir_path)

    return avatar_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=user_avatar_directory_path,
        help_text="Your avatar image.",
    )
    bio = models.TextField(max_length=325, blank=True, null=True, help_text="Your bio")

    def __str__(self):
        return f"{self.user.username} Profile."

    def avatar(self):
        if self.image:
            return self.image.url
        else:
            return default_avatar_url.format(username=self.user.username)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            fixed_height = 300
            image = Image.open(self.image.path)
            height_percent = fixed_height / float(image.size[1])
            width_size = int((float(image.size[0]) * float(height_percent)))
            image = image.resize((width_size, fixed_height), Image.NEAREST)
            image.save(self.image.path)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
