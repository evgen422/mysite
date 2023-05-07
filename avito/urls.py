from django.urls import path
from avito.views import img_view
from avito.views import single_car_view


from . import views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('image/<str:car_id>/', img_view, name='img_view'),
    path('<str:car_id>/', single_car_view, name='single_car_view'),

]
