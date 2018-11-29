from django.urls import path

from . import views
app_name = 'video'

urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.VideoListView.as_view(), name='list'),
    path('watch/<pk>', views.VideoDetailView.as_view(), name='watch'),
    path('new', views.AddVideoView.as_view(), name='add'),
]
