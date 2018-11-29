from django.shortcuts import render, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .models import Video


def index(*args, **kwargs):
    return VideoListView.as_view()(*args, **kwargs)


class VideoListView(ListView):
    '''
    List the most recent public videos
    '''

    model = Video
    template_name = 'video/list.html'
    context_object_name = 'videos'

    def get_queryset(self):
        '''
        Custom queryset to fetch only public videos
        '''

        return self.model.objects.filter(visibility='PUBLIC').order_by('-created')


class VideoDetailView(DetailView):
    '''
    Watch video page
    '''

    model = Video
    template_name = 'video/watch.html'


class AddVideoView(CreateView):
    model = Video
    template_name = 'video/add.html'
    fields = ['title', 'video_file', 'visibility', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('video:watch', args=(self.object.pk,))
