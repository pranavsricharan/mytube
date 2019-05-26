from django.contrib import admin

from .models import Playlist, PlaylistVideoMapping

admin.site.register([Playlist, PlaylistVideoMapping])
