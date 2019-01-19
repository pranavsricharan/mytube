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

    def rate_video(self, user: User, rating: str):
        try:
            # Update rating if already rated
            video_rating = VideoRating.objects.get(video=self, user=user)
            video_rating.rating = rating
            video_rating.save()
        except:
            VideoRating(video=self, user=user, rating=rating).save()

    def like_count(self):
        return VideoRating.objects.filter(video=self, rating='LIKE').count()

    def dislike_count(self):
        return VideoRating.objects.filter(video=self, rating='DISLIKE').count()

    def like_percentage(self):
        like_count = self.like_count()
        try:
            return like_count / (like_count + self.dislike_count()) * 100
        except ArithmeticError:
            return 100

    def user_rating(self, user, get_rating_object=False):
        print(user)
        try:
            rating = VideoRating.objects.get(video=self, user=user)
            if not get_rating_object:
                rating = rating.rating
            print(rating)
            return rating
        except:
            import traceback
            traceback.print_exc()
            return None

    def __str__(self):
        return '<{}> {}'.format(self.id, self.title)


class Comment(models.Model):
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE)
    watched_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-watched_time']
        verbose_name_plural = 'history entries'

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.video.id)


class VideoRating(models.Model):
    RATING = (('LIKE', 'Like'), ('DISLIKE', 'Dislike'))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE)
    rating = models.CharField(max_length=7, choices=RATING, default='LIKE')


class Playlist(models.Model):
    VISIBILITY = (
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='Untitled Playlist')
    visibility = models.CharField(
        max_length=7, default='PUBLIC', choices=VISIBILITY)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # False for system created playlists like favorites and watch later
    deletable = models.BooleanField(default=True)

    class Meta:
        ordering = ['deletable']

    def __str__(self):
        return '[{}] {} <{}>'.format(self.visibility, self.name, self.user)

    def add_video(self, video: Video) -> None:
        try:
            # Check if already exists
            PlaylistVideoMapping.objects.get(playlist=self, video=video)
        except:
            PlaylistVideoMapping(playlist=self, video=video).save()

    def remove_video(self, video: Video) -> None:
        try:
            PlaylistVideoMapping.objects.get(
                playlist=self, video=video).delete()
        except:
            return

    def has_video(self, video: Video) -> bool:
        try:
            PlaylistVideoMapping.objects.get(playlist=self, video=video)
            return True
        except:
            return False

    def length(self):
        return PlaylistVideoMapping.objects.filter(playlist=self).count()

    def get_videos(self, n=4):
        video_ids = PlaylistVideoMapping.objects.filter(
            playlist=self).values_list('video', flat=True).distinct()[:n]

        return Video.objects.filter(id__in=video_ids)


class PlaylistVideoMapping(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
