from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User

from .models import Video, Comment


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

    def get_object(self, queryset=None):
        video_object: Video = super(
            VideoDetailView, self).get_object(queryset=queryset)
        if self.request.method == 'GET':
            video_object.increment_view_count()
            video_object.save()
            video_object.refresh_from_db()
        return video_object


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


class UserVideoListView(ListView):
    '''
    - List the public videos of any user
    - List all the videos of the logged in user
    '''

    model = Video
    template_name = 'video/channel.html'
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


class AddCommentView(CreateView):
    model = Comment
    template_name = 'video/add_comment.html'
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.video = get_object_or_404(Video, id=self.kwargs.get('pk'))
        form.instance.video = self.video
        form.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('video:watch', args=(self.video.pk,))
