from django.contrib.auth.models import AbstractUser
from django.db import models


class UserApp(AbstractUser):
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.username
