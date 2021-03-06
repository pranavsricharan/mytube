import datetime

from django.shortcuts import reverse, get_object_or_404, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Video, Comment, History, VideoRating
from mytube.apps.playlist.models import Playlist


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

    def get_context_data(self, **kwargs):
        context_data = super(VideoDetailView, self).get_context_data(**kwargs)

        playlists = []

        if self.request.user.is_authenticated:
            for playlist in Playlist.objects.filter(user=self.request.user).order_by('deletable'):
                playlists.append({
                    'id': playlist.id,
                    'name': playlist.name,
                    'has_video': playlist.has_video(context_data['video'])
                })

        context_data['playlists'] = playlists
        return context_data


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
