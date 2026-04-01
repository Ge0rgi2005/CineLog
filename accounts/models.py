from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    bio = models.TextField(
        blank=True,
        null=True,
        help_text="Write a brief description of your profile here.",
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username