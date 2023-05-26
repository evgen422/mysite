from django.urls import path
from opencv.views import video_feed


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('opencv/video_feed/<str:user_id>/', video_feed, name='video_feed'),
    path('ping/', views.ping, name='ping'),

]
