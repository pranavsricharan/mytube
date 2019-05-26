from django.apps import AppConfig


class PlaylistConfig(AppConfig):
    name = 'playlist'

    def ready(self):
        import mytube.apps.playlist.signals
