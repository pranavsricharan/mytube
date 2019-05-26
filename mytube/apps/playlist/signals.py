from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Playlist
@receiver(signal=post_save, sender=User)

def create_default_playlists(sender, instance, created, **kwargs):
    try:
        # User updation
        Playlist.objects.get(name='Watch later',
                             deletable=False, user=instance)
    except:
        # User creation
        Playlist(name='Watch later', deletable=False,
                 user=instance, visibility='PRIVATE').save()
        Playlist(name='Favourites', deletable=False,
                 user=instance, visibility='PRIVATE').save()
