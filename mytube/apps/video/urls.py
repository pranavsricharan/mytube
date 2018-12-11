from django.urls import path

from . import views
app_name = 'video'

urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.VideoListView.as_view(), name='list'),
    path('v/<pk>', views.VideoDetailView.as_view(), name='watch'),
    path('v/<pk>/add_comment', views.AddCommentView.as_view(), name='add_comment'),
    path('new', views.AddVideoView.as_view(), name='add'),
    path('history', views.HistoryListView.as_view(), name='history'),
    path('u/<str:username>', views.UserVideoListView.as_view(), name='channel'),
]
