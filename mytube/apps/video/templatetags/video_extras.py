from django import template
from datetime import timedelta

register = template.Library()


@register.simple_tag
def get_duration(seconds):
    formatted_duration = str(timedelta(0, seconds))
    while formatted_duration[0] in ['0', ':']:
        formatted_duration = formatted_duration[1:]

    return formatted_duration
