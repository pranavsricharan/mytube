from django.urls import path

from . import views
app_name = 'feed'

urlpatterns = [
    path('', views.MainFeedView.as_view(), name='index'),
    path('history', views.HistoryListView.as_view(), name='history'),
    path('liked', views.LikedVideosListView.as_view(), name='liked'),
    path('most-viewed', views.MostViewedListView.as_view(), name='most-viewed'),
    path('top', views.TopRatedListView.as_view(), name='top'),
]
