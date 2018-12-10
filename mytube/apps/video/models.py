from hashlib import md5
from time import time
import uuid

from django.db import models
from django.contrib.auth.models import User


def get_bucket() -> str:
    number_str: str = str(int(time()) % 100)
    bucket: str = md5(number_str.encode()).hexdigest()
    return bucket


def video_upload_to(video: models.Model, filename: str) -> str:
    video.original_file_name = filename

    if '.' not in filename:
        ext = 'mp4'
    else:
        ext = filename[filename.rfind('.') + 1:]

    return 'uploads/{}/{}.{}'.format(get_bucket(), str(uuid.uuid4()), ext)


def thumb_upload_to(video: models.Model, filename: str) -> str:
    return 'thumbs/{}/{}.jpg'.format(get_bucket(), video.id)


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

    duration = models.IntegerField(null=True, blank=True)
    views = models.IntegerField(default=0)

    preview_thumb = models.FileField(
        null=True, blank=True, upload_to=thumb_upload_to)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='videos')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def increment_view_count(self):
        self.views = models.F('views') + 1

    def __str__(self):
        return '<{}> {}'.format(self.id, self.title)


class Comment(models.Model):
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
