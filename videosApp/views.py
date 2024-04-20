import json
from django.shortcuts import render, HttpResponse, get_list_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from .models import Video, Playlist, Category


class VideoListView(ListView):
    template_name = "videos/videos.html"
    model = Video


class VideoDetailView(DetailView):
    template_name = "videos/video_detail.html"
    model = Video


class VideoDelete(DeleteView):
    model = Video
    success_url = reverse_lazy("videos")
    template_name = "standardForm\delete.html"


def playlist_list(request):
    playlists = Playlist.objects.all()
    context = {"object_list": []}
    for playlist in playlists:
        video = playlist.videos.first() if playlist.videos.exists() else None
        context["object_list"].append(
            {
                "pk": playlist.pk,
                "title": playlist.title,
                "description": playlist.description,
                "created_at": playlist.created_at,
                "preview": video.preview,
            }
        )
    return render(request, "playlist/playlists.html", context)


class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = "playlist/playlist_detail.html"

    def get_object(self):
        pk = self.kwargs.get("pk")
        playlist = Playlist.objects.get(pk=pk)
        return playlist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist = self.get_object()
        videos = playlist.videos.all()
        context["videos"] = videos
        return context


def delete_video_playlist(request, playlist_pk, pk):
    playlist_obj = Playlist.objects.get(pk=playlist_pk)  # получаем объект плейлиста

    video_obj = Video.objects.get(pk=pk)  # получаем объект видео

    playlist_obj.videos.remove(video_obj)  # удаляем видео из плейлиста
    playlist_obj.save()  # сохраняем изменения в базе данных
    return redirect(reverse_lazy("playlist_list"))


class PlaylistDelete(DeleteView):
    model = Playlist
    success_url = reverse_lazy("playlists")
    template_name = "standardForm\delete.html"
