from django.contrib import admin

from .models import Video, Comment, History

admin.site.register([Video, Comment, History])
