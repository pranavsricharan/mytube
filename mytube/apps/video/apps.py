from django.apps import AppConfig


class VideoConfig(AppConfig):
    name = 'mytube.apps.video'

    def ready(self):
        import mytube.apps.video.signals
