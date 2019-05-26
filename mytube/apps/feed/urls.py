from django.urls import path

from . import views
app_name = 'feed'

urlpatterns = [
    path('', views.VideoListView.as_view(), name='index'),
    path('history', views.HistoryListView.as_view(), name='history'),
]
