from django.contrib import admin

from .models import Video, Comment, History, Playlist, VideoRating, PlaylistVideoMapping

admin.site.register([Video, Comment, History, VideoRating,
                     Playlist, PlaylistVideoMapping])
