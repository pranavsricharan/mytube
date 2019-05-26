from django.urls import path

from . import views
app_name = 'playlist'

urlpatterns = [
    path('add', views.add_to_playlist, name='add'),
    path('watch-later', views.WatchLaterListView.as_view(), name='watch_later'),
    path('favourites', views.FavouritesListView.as_view(), name='favourites'),
    path('<pk>', views.PlaylistDetailView.as_view(), name='detail'),
]
