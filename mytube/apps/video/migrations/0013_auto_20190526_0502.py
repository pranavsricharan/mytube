# Generated by Django 2.1.3 on 2019-05-26 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0012_playlist_playlistvideomapping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='user',
        ),
        migrations.RemoveField(
            model_name='playlistvideomapping',
            name='playlist',
        ),
        migrations.RemoveField(
            model_name='playlistvideomapping',
            name='video',
        ),
        migrations.DeleteModel(
            name='Playlist',
        ),
        migrations.DeleteModel(
            name='PlaylistVideoMapping',
        ),
    ]
