from django import template
from datetime import timedelta
import re


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


@register.filter(name='format_text')
def format_text(text):
    return URL_PATTERN.sub(r'<a href="\1" target="_blank">\1</a>', text)
