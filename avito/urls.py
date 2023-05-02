from django.urls import path
from avito.views import img_view


from . import views

urlpatterns = [
    #path("", views.index, name="cars"),
    path('car-list/', views.car_list, name='car_list'),
    path('image/<str:car_id>/', img_view, name='img_view'),

]
