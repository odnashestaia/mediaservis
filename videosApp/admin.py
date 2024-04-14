from django.contrib import admin

from .models import Video, Playlist, Category

admin.site.register(Video)
admin.site.register(Playlist)
admin.site.register(Category)
