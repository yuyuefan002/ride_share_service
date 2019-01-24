from django.urls import path
from .import views

app_name = 'orders'
urlpatterns =[
    path('', views.index, name='index'),
    path('driver-register/', views.DriverRegister, name='driver_register'),
    path('ride-request/', views.RideRequest, name='ride_request'),
    path('driver-register-error/', views.DriverRegisterErr, name='driver_register_error'),
    path('requests/', views.RequestListView.as_view(), name='requests'),
    path('requests/<uuid:pk>/', views.RideRequestEditing, name='ride_request_editing'),
]
