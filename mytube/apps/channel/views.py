from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth.models import User

from mytube.apps.video.models import Video
from mytube.apps.playlist.models import Playlist

class UserVideoListView(ListView):
    '''
    - List the public videos of any user
    - List all the videos of the logged in user
    '''

    model = Video
    template_name = 'channel/index.html'
    context_object_name = 'videos'

    def get_queryset(self):
        '''
        Custom queryset to fetch only public videos
        '''

        username = self.kwargs.get('username')
        if self.request.user.username == username:
            self.user = self.request.user
            return self.model.objects.filter(user=self.request.user).order_by('-created')

        self.user = get_object_or_404(User, username=username)
        return self.model.objects.filter(user=self.user, visibility='PUBLIC').order_by('-created')

    def get_context_data(self, *args, **kwargs):
        context_data = super(
            UserVideoListView, self).get_context_data(*args, **kwargs)
        context_data['channel_user'] = self.user
        return context_data


class PlaylistListView(UserVideoListView):
    model = Playlist
    context_object_name = 'playlists'
    template_name = 'channel/playlist.html'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        self.user = user
        if self.request.user.id == user.id:
            return Playlist.objects.filter(user=self.request.user)

        return Playlist.objects.filter(user=user, visibility='PUBLIC')