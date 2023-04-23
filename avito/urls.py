from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="cars"),
    path('car-list/', views.car_list, name='car_list'),

]