import re

from django import template
from datetime import timedelta

from ..models import Playlist, PlaylistVideoMapping

URL_PATTERN = re.compile(r'(https?://[^\s]+)')
register = template.Library()


@register.simple_tag
def get_duration(seconds):
    try:
        formatted_duration = str(timedelta(0, seconds))
        while formatted_duration[0] in ['0', ':']:
            formatted_duration = formatted_duration[1:]

        return formatted_duration
    except:
        return '--:--'


@register.simple_tag
def user_rating(video, user):
    return video.user_rating(user)


@register.simple_tag
def user_watch_later_id(user):
    try:
        return Playlist.objects.get(name='Watch later', user=user, deletable=False).id
    except:
        return None


@register.simple_tag
def user_favourites_id(user):
    try:
        return Playlist.objects.get(name='Favourites', user=user, deletable=False).id
    except:
        return None


@register.simple_tag
def is_in_playlist(video, playlist):
    try:
        PlaylistVideoMapping.objects.get(
            video__id=video, playlist__id=playlist)
        return True
    except:
        return False


@register.filter(name='format_text')
def format_text(text):
    return URL_PATTERN.sub(r'<a href="\1" target="_blank">\1</a>', text)
