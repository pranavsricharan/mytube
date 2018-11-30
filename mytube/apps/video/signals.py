from tempfile import TemporaryDirectory
from os import system
from random import randint

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File

from .models import Video


@receiver(post_save, sender=Video)
def create_preview_thumb(sender, instance, created, **kwargs):
    print('Generating thumbs')
    print(created, bool(instance.preview_thumb), type(instance.preview_thumb))
    if created and bool(instance.preview_thumb) == False:
        with TemporaryDirectory() as temp_dir:
            system('ffprobe -i "{0}" -show_entries format=duration -v quiet -of csv="p=0" > {1}/tmp'.format(
                instance.video_file.path, temp_dir))

            duration = 0
            with open(temp_dir + '/tmp') as f:
                duration = float(f.read().strip()) // 1 + 1
            instance.duration = duration

            random_frame_range = 59 if duration >= 60 else duration
            random_frame = randint(1, random_frame_range)

            system('ffmpeg -i "{0}" -an -y -ss 00:00:{1} -f mjpeg -vframes 1 "{2}/thumb.jpg"'.format(
                instance.video_file.path, random_frame, temp_dir))

            with open(temp_dir + '/thumb.jpg', 'rb') as f:
                django_file = File(f)
                instance.preview_thumb = django_file
                instance.save()
