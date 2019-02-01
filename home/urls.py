from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('loginHome/', views.loginHome, name='loginHome'),
    path('ownerHome/', views.ownerHome, name='ownerHome'),
    path('driverHome/', views.driverHome, name='driverHome'),
    path('sharerHome/', views.sharerHome, name='sharerHome'),
]
