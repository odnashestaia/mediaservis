from django.urls import path
from .views import (
    VideoDetailView,
    VideoListView,
    VideoDelete,
    PlaylistDelete,
    PlaylistDetailView,
    playlist_list,
    delete_video_playlist,
)


urlpatterns = [
    path("", VideoListView.as_view(), name="videos"),
    path("video/<int:pk>", VideoDetailView.as_view(), name="video-detail"),
    path("video/<int:pk>/delete", VideoDelete.as_view(), name="video-delete"),
    path("playlists", playlist_list, name="playlists"),
    path("playlist/<int:pk>", PlaylistDetailView.as_view(), name="playlist-detail"),
    path("playlist/delete/<int:pk>", PlaylistDelete.as_view(), name="playlist-delete"),
    path(
        "playlist/<int:playlist_pk>/video/delete/<int:pk>",
        delete_video_playlist,
        name="playlist-delete-video",
    ),
]
