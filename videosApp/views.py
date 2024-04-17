from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Video, Playlist, Category


class VideoListView(ListView):
    template_name = "videos/videos.html"
    model = Video


class VideoDetailView(DetailView):
    template_name = "videos/video_detail.html"
    model = Video
