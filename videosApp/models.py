from django.db import models
from userApp.models import UserApp


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="videos")
    duration = models.DurationField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        UserApp, on_delete=models.CASCADE, related_name="uploaded_videos"
    )
    likes = models.ManyToManyField(UserApp, related_name="liked_videos", blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.title


class Playlist(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        UserApp, on_delete=models.CASCADE, related_name="playlists"
    )
    videos = models.ManyToManyField(Video, related_name="playlists", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
