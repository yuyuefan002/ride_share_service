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
    path('ride-search/', views.RideSearchingListView.as_view(), name='ride_search'),
    path('cf-ride-status', views.CFRideStatusListView.as_view(), name='cf_ride_status'),
    path('cf-ride-detail/<uuid:pk>', views.CFRideDetail, name='cf_ride_detail'),
    path('driver-check/', views.DriverCheck, name='driver_check'),
    path('ride-confirm/<uuid:pk>/', views.RideConfirm, name='ride_confirm'),
    path('share-ride-request/', views.ShareRideRequest, name='share_ride_request'),
    path('share-ride_list/<uuid:pk>/', views.ShareRideSearchingListView.as_view(), name='share_ride_list'),
    path('share-ride-confirm/<uuid:main_id>', views.ShareRideConfirm, name='share_ride_confirm'),
    path('cf-ride-request-check/<uuid:pk>/', views.CFRideRequestCheck, name='cf_ride_request_check'),
    path('ride-request-status-jump/<uuid:pk>/', views.RideRequestJump, name='ride_request_jump'),
]
