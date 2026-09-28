from django.urls import path

from . import views

urlpatterns = [
    path('', views.car_counting, name='car_counting'),
    #path('opencv/video_feed/<str:user_id>/', video_feed, name='video_feed'),
    #path('ping/', views.ping, name='ping'),
]
