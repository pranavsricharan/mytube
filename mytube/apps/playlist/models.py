import uuid
from django.db import models
from django.contrib.auth.models import User

from mytube.apps.video.models import Video

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
