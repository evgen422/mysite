from django.urls import path
from opencv.views import video_feed


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('ping/', views.ping, name='ping'),

]
