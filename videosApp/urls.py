from django.urls import path

from .views import (
    PlaylistDelete,
    PlaylistDetailView,
    playlist_list,
    delete_video_playlist,
    PlaylistUpdateView,
    PlaylistCreateView,
    add_video_playlist,
)

from .views import VideoDetailView, VideoListView, VideoDelete, VideoCreate, video_list

from .views import (
    CategoryCreateView,
)

urlpatterns = []


video = [
    path("", VideoListView.as_view(), name="videos"),
    path("video/<int:pk>", VideoDetailView.as_view(), name="video-detail"),
    path("video/<int:pk>/delete", VideoDelete.as_view(), name="video-delete"),
    path("video/add", VideoCreate.as_view(), name="video-add"),
    path("video/test", video_list, name="video-test"),
]

playlist = [
    path("playlists", playlist_list, name="playlists"),
    path("playlist/<int:pk>", PlaylistDetailView.as_view(), name="playlist-detail"),
    path("playlist/delete/<int:pk>", PlaylistDelete.as_view(), name="playlist-delete"),
    path(
        "playlist/<int:pk>/video/delete/<int:video_pk>",
        delete_video_playlist,
        name="playlist-delete-video",
    ),
    path("playlist/create", PlaylistCreateView.as_view(), name="playlist-create"),
    path(
        "playlist/add/video/<int:pk>",
        add_video_playlist,
        name="playlist-add-video",
    ),
    path(
        "playlist/<int:pk>/update", PlaylistUpdateView.as_view(), name="playlist-update"
    ),
]

category = [
    path("category/create", CategoryCreateView.as_view(), name="category-create")
]


urlpatterns += video + playlist + category
