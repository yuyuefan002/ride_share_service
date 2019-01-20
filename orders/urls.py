from django.urls import path
from .import views

app_name = 'orders'
urlpatterns =[
    path('', views.index, name='index'),
#    path('driver-register', views.DriverRegister, name='driver_register')
]
