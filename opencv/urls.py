from django.urls import path

from . import views

urlpatterns = [
    path('', views.car_counting, name='car_counting'),
    path('live-stream/', views.live_stream, name='live_stream'),
    path('live-stream/status/', views.live_stream_status, name='live_stream_status'),
    path('live-stream/feed/', views.live_stream_feed, name='live_stream_feed'),
    path('live-stream/yolo-stats/', views.live_stream_stats, name='live_stream_yolo_stats'),

    #path('opencv/video_feed/<str:user_id>/', video_feed, name='video_feed'),
    #path('ping/', views.ping, name='ping'),
]
