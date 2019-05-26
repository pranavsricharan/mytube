from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from mytube.apps.video.models import Video, History, VideoRating


class MainFeedView(ListView):
    '''
    List the most recent public videos
    '''

    model = Video
    template_name = 'feed/index.html'
    context_object_name = 'videos'

    def get_queryset(self):
        '''
        Custom queryset to fetch only public videos
        '''

        return self.model.objects.filter(visibility='PUBLIC').order_by('-created')


class VideoListView(ListView):
    template_name = 'feed/list.html'
    context_object_name = 'entries'
    list_title = ''

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['list_title'] = self.list_title
        return context


class AuthRequiredVideoListView(LoginRequiredMixin, VideoListView):
    login_url = reverse_lazy('account:login')

    def get_queryset(self):
        '''
        Custom queryset to fetch user's history
        '''

        return self.model.objects.filter(user=self.request.user)

class HistoryListView(AuthRequiredVideoListView):
    '''
    List the user's history
    '''
    list_title = 'History'
    model = History


class LikedVideosListView(AuthRequiredVideoListView):
    '''
    List the user's liked videos
    '''
    list_title = 'Liked Videos'
    model = VideoRating
    