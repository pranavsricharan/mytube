from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from mytube.apps.video.models import Video, History


class VideoListView(ListView):
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


class HistoryListView(LoginRequiredMixin, ListView):
    '''
    List the most recent public videos
    '''

    login_url = reverse_lazy('account:login')
    model = History
    template_name = 'feed/history.html'
    context_object_name = 'entries'

    def get_queryset(self):
        '''
        Custom queryset to fetch user's history
        '''

        return self.model.objects.filter(user=self.request.user)
