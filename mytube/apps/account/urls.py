from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.login, name='login'),
    path('create', views.register, name='register'),
    path('logout', views.logout, name='logout'),
]
