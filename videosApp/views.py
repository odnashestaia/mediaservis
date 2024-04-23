from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView
from .models import Video, Playlist, Category
# from .form import CreatePlaylistForm
# from userApp.models import UserApp


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
                "created_at": playlist.created_at,
                "preview": video.preview if playlist.videos.exists() else "#",
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


def delete_video_playlist(request, pk, video_pk):
    playlist_obj = Playlist.objects.get(pk=pk)  # получаем объект плейлиста

    video_obj = Video.objects.get(pk=video_pk)  # получаем объект видео

    playlist_obj.videos.remove(video_obj)  # удаляем видео из плейлиста
    playlist_obj.save()  # сохраняем изменения в базе данных
    return redirect(reverse_lazy("playlist_list"))


class PlaylistDelete(DeleteView):
    model = Playlist
    success_url = reverse_lazy("playlists")
    template_name = "standardForm\delete.html"


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    fields = ["title", "category"]
    template_name = "playlist\create_playlist.html"
    success_url = reverse_lazy("playlists")

    def form_valid(self, form):
        """при валидации добавляем создателя"""
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        """добавляем категории для вывода"""
        context = super().get_context_data(**kwargs)
        context["categorys"] = Category.objects.all()
        return context
