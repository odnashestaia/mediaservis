from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django_htmx.http import HttpResponseClientRefresh
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    CreateView,
    UpdateView,
)
from .models import Video, Playlist, Category


"""  Videos  """


class VideoListView(LoginRequiredMixin, ListView):
    template_name = "videos/list.html"
    model = Video


class VideoDetailView(LoginRequiredMixin, DetailView):
    template_name = "videos/detail.html"
    model = Video


class VideoDelete(LoginRequiredMixin, DeleteView):
    model = Video
    success_url = reverse_lazy("videos")
    template_name = "standardForm\delete.html"


class VideoCreate(LoginRequiredMixin, CreateView):
    model = Video
    fields = ["title", "category", "description", "preview", "duration", "file"]
    template_name = "videos/add.html"
    success_url = reverse_lazy("videos")

    def form_valid(self, form):
        """при валидации добавляем создателя"""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        """добавляем категории для вывода"""
        context = super().get_context_data(**kwargs)
        context["categorys"] = Category.objects.all()
        return context


"""  playlist  """


@login_required
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
                "preview": video.preview if playlist.videos.exists() else "",
            }
        )
    return render(request, "playlist/list.html", context)


class PlaylistDetailView(LoginRequiredMixin, DetailView):
    model = Playlist
    template_name = "playlist/detail.html"

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


@login_required
def delete_video_playlist(request, pk, video_pk):
    playlist_obj = Playlist.objects.get(pk=pk)  # получаем объект плейлиста

    video_obj = Video.objects.get(pk=video_pk)  # получаем объект видео

    playlist_obj.videos.remove(video_obj)  # удаляем видео из плейлиста
    playlist_obj.save()  # сохраняем изменения в базе данных
    return redirect(reverse_lazy("playlists"))


class PlaylistDelete(LoginRequiredMixin, DeleteView):
    model = Playlist
    success_url = reverse_lazy("playlists")
    template_name = "standardForm\delete.html"


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    fields = ["title", "category"]
    template_name = "playlist\create.html"
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


class PlaylistUpdateView(LoginRequiredMixin, UpdateView):
    model = Playlist
    fields = ["title", "category"]
    template_name = "playlist/create.html"
    success_url = reverse_lazy("playlists")

    def get_context_data(self, *, object_list=None, **kwargs):
        """добавляем категории для вывода"""
        context = super().get_context_data(**kwargs)
        playlist = Playlist.objects.get(id=self.object.pk)
        context["categorys"] = Category.objects.all()
        context["category_id"] = playlist.category.pk
        context["title"] = playlist.title
        print(context)
        return context


@login_required
@require_http_methods(["GET", "POST"])
def add_video_playlist(request, pk):
    if request.method == "POST":
        video = get_object_or_404(Video, pk=pk)
        playlist = get_object_or_404(Playlist, pk=request.POST.get("playlist"))
        playlist.videos.add(video)
        return HttpResponseClientRefresh()
    else:
        playlist_list = Playlist.objects.filter(owner=request.user.pk)
        video = get_object_or_404(Video, pk=pk)
        return render(
            request,
            "playlist/add_video.html",
            {"playlist_list": playlist_list, "video": video},
        )


""" категории """


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ["name"]
    template_name = "standardForm/add_category.html"
    success_url = reverse_lazy("playlists")

    def form_valid(self, form):
        if not Category.objects.filter(name=form.instance.name):
            return super().form_valid(form)
        else:
            form.add_error(None, "Уже существует")
            return self.render_to_response(self.get_context_data(form=form))
