from django.urls import path

from . import views
app_name = 'video'

urlpatterns = [
    path('<pk>', views.VideoDetailView.as_view(), name='watch'),
    path('<pk>/add_comment', views.AddCommentView.as_view(), name='add_comment'),
    path('<pk>/rate', views.rate_video, name='rate_video'),
    path('new', views.AddVideoView.as_view(), name='add'),
]
