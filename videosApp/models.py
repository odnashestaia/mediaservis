from django.db import models
from userApp.models import UserApp


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="videos")
    preview = models.FileField(upload_to="preview", blank=True)
    duration = models.DurationField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        UserApp, on_delete=models.CASCADE, related_name="uploaded_videos"
    )
    likes = models.ManyToManyField(UserApp, related_name="liked_videos", blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    def total_likes(self):
        # подсчет лайков
        return self.likes.count()


class Playlist(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(
        UserApp, on_delete=models.CASCADE, related_name="owner_playlists"
    )
    videos = models.ManyToManyField(Video, related_name="videos_playlists", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
