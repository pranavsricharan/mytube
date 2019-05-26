from django.urls import path

from . import views

app_name = 'channel'

urlpatterns = [
    path('<str:username>', views.UserVideoListView.as_view(), name='index'),
    path('<str:username>/playlists',
         views.PlaylistListView.as_view(), name='playlists')
]
