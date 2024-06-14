from django.contrib.auth.models import User
from django.db import models


class Video(models.Model):
    # создание модели videos
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="videos")
    preview = models.FileField(upload_to="preview", blank=True)
    duration = models.DurationField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="uploaded_videos"
    )
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Playlist(models.Model):
    # Создание модели Playlist
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner_playlists"
    )
    videos = models.ManyToManyField(Video, related_name="videos_playlists", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    # Создание модели Category
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
