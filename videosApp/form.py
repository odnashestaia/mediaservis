from django import forms
from userApp.models import UserApp
from .models import Playlist, Category


class CreatePlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ["title", "owner", "category"]
