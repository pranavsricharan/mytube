import datetime

from django.shortcuts import render, reverse, get_object_or_404, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Video, Comment, History, VideoRating


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

        if video_object.visibility == 'PRIVATE' and video_object.user.id != self.request.user.id:
            raise Http404

        if self.request.user.is_authenticated:
            # Increment video view count and reload object
            video_object.increment_view_count()
            video_object.save()
            video_object.refresh_from_db()

            # Create new entry in user history
            try:
                user_last_viewed_video: History = History.objects.get(
                    user=self.request.user, video=video_object)
                user_last_viewed_video.watched_time = datetime.datetime.now()
                user_last_viewed_video.save()
            except:
                import traceback
                traceback.print_exc()
                History(user=self.request.user, video=video_object).save()
        return video_object


class AddVideoView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('account:login')
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


class AddCommentView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('account:login')
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


@login_required(login_url=reverse_lazy('account:login'))
def rate_video(request, pk):
    if request.method == 'POST':
        rating = request.POST.get('rating')

        if rating not in ['LIKE', 'DISLIKE']:
            rating = 'LIKE'

        video: Video = get_object_or_404(
            Video, id=pk, visibility__in=['PUBLIC', 'UNLISTED'])
        video_rating = video.user_rating(request.user, get_rating_object=True)

        if video_rating is not None:
            # If user has already rated the video delete the previously
            # rated item

            if video_rating.rating != rating:
                # Create new rating only if the previously rated value
                # is not being toggled

                VideoRating(user=request.user, video=video,
                            rating=rating).save()

            video_rating.delete()
        else:
            VideoRating(user=request.user, video=video, rating=rating).save()

        return HttpResponseRedirect(reverse('video:watch', kwargs={'pk': video.pk}))

    raise Http404


class HistoryListView(LoginRequiredMixin, ListView):
    '''
    List the most recent public videos
    '''

    login_url = reverse_lazy('account:login')
    model = History
    template_name = 'video/history.html'
    context_object_name = 'entries'

    def get_queryset(self):
        '''
        Custom queryset to fetch user's history
        '''

        return self.model.objects.filter(user=self.request.user)
