from django.urls import path

from . import views
app_name = 'feed'

urlpatterns = [
    path('', views.VideoListView.as_view(), name='index'),
    path('history', views.HistoryListView.as_view(), name='history'),
    path('liked', views.LikedVideosListView.as_view(), name='liked'),
]
