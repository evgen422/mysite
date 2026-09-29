"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from opencv import views as opencv_views

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("portfolio/", include("portfolio.urls")),
    path("avito/", include("avito.urls")),
    path("opencv/", include("opencv.urls")),
    path("live-stream/", opencv_views.live_stream, name="live_stream_root"),
    path("live-stream/feed/", opencv_views.live_stream_feed, name="live_stream_feed_root"),
    path("live-stream/status/", opencv_views.live_stream_status, name="live_stream_status_root"),
    path("live-stream/yolo-stats/", opencv_views.live_stream_stats, name="live_stream_yolo_stats_root"),

]

