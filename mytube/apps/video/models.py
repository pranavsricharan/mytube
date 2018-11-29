from hashlib import md5
from time import time
import uuid

from django.db import models
from django.contrib.auth.models import User


def video_upload_to(video: models.Model, filename: str) -> str:
    video.original_file_name = filename

    number_str: str = str(int(time()) % 100)
    bucket: str = md5(number_str.encode()).hexdigest()

    if '.' not in filename:
        ext = 'mp4'
    else:
        ext = filename[filename.rfind('.') + 1:]

    return 'uploads/{}/{}.{}'.format(bucket, str(uuid.uuid4()), ext)


class Video(models.Model):
    VISIBILITY = (
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('UNLISTED', 'Unlisted'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255, default='Untitled Video')
    description = models.TextField(null=True, blank=True)

    video_file = models.FileField(upload_to=video_upload_to)
    original_file_name = models.CharField(
        max_length=512, default='', blank=True)

    visibility = models.CharField(
        max_length=8, default='PUBLIC', choices=VISIBILITY)
    views = models.IntegerField(default=0)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='videos')
    created = models.DateTimeField(auto_now_add=True)
