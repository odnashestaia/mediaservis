from django_filters import FilterSet, CharFilter

from .models import Playlist, Video


class VideoFilter(FilterSet):
    category = CharFilter(field_name="category__name", lookup_expr="icontains")

    class Meta:
        model = Video
        fields = ["category"]


class PlaylistFilter(FilterSet):
    category = CharFilter(field_name="category__name", lookup_expr="icontains")

    class Meta:
        model = Playlist
        fields = ["category"]
