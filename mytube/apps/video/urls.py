from django.urls import path

from . import views
app_name = 'video'

urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.VideoListView.as_view(), name='list'),
    path('v/<pk>', views.VideoDetailView.as_view(), name='watch'),
    path('v/<pk>/add_comment', views.AddCommentView.as_view(), name='add_comment'),
    path('v/<pk>/rate', views.rate_video, name='rate_video'),
    path('new', views.AddVideoView.as_view(), name='add'),
    path('history', views.HistoryListView.as_view(), name='history'),
    path('p/add', views.add_to_playlist, name='playlist_add'),
    path('p/<pk>', views.PlaylistDetailView.as_view(), name='playlist_detail'),
    path('watch-later', views.WatchLaterListView.as_view(), name='watch_later'),
    path('favourites', views.FavouritesListView.as_view(), name='favourites'),

]
