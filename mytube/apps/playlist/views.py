from django.shortcuts import get_object_or_404, Http404, HttpResponseRedirect, reverse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from mytube.apps.video.models import Video
from .models import Playlist, PlaylistVideoMapping

class PlaylistDetailView(ListView):
    '''
    List the videos of a playlist
    '''

    model = PlaylistVideoMapping
    template_name = 'playlist/detail.html'
    context_object_name = 'entries'

    def get_queryset(self):
        '''
        Custom queryset to fetch playlist
        '''

        if self.kwargs.get('pk') is not None:
            self.id = self.kwargs.get('pk')

        self.playlist: Playlist = get_object_or_404(Playlist, id=self.id)

        if self.playlist.visibility == 'PRIVATE' and self.playlist.user != self.request.user:
            raise Http404

        return self.model.objects.filter(playlist=self.playlist)

    def get_context_data(self, *args, **kwargs):
        context_data = super(
            PlaylistDetailView, self).get_context_data(*args, **kwargs)
        context_data['playlist'] = self.playlist

        return context_data


class WatchLaterListView(LoginRequiredMixin, PlaylistDetailView):
    login_url = reverse_lazy('account:login')

    def dispatch(self, *args, **kwargs):
        self.id = Playlist.objects.get(
            deletable=False, name='Watch later', user=self.request.user).id
        return super(WatchLaterListView, self).dispatch(*args, **kwargs)


class FavouritesListView(LoginRequiredMixin, PlaylistDetailView):
    login_url = reverse_lazy('account:login')

    def dispatch(self, *args, **kwargs):
        self.id = Playlist.objects.get(
            deletable=False, name='Favourites', user=self.request.user).id
        return super(FavouritesListView, self).dispatch(*args, **kwargs)


@login_required(login_url=reverse_lazy('account:login'))
def add_to_playlist(request):
    if request.method == 'POST':
        video_pk = request.POST.get('video_pk')
        playlist_pk = request.POST.get('playlist_pk')

        video = get_object_or_404(Video, id=video_pk)

        if playlist_pk is None:
            # Create new playlist
            name = request.POST.get('name', 'Untitled Playlist')
            visibility = request.POST.get('visibility', 'PUBLIC')

            playlist: Playlist = Playlist(
                name=name, user=request.user, visibility=visibility)
            playlist.save()
        else:
            playlist: Playlist = get_object_or_404(
                Playlist, id=playlist_pk, user=request.user)

        if playlist.has_video(video):
            playlist.remove_video(video)
        else:
            playlist.add_video(video)

    return HttpResponseRedirect(reverse('video:watch', args=(video_pk,)))
