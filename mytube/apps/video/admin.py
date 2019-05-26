from django.contrib import admin

from .models import Video, Comment, History, VideoRating

admin.site.register([Video, Comment, History, VideoRating])
