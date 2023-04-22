from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="cars"),
    path('top-makes/', views.top_makes, name='top_makes'),

]