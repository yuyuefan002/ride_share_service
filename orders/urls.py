from django.urls import path
from .import views

app_name = 'orders'
urlpatterns =[
    path('', views.index, name='index'),
    path('driver/register/', views.DriverRegister, name='driver_register'),
    path('driver/profile/', views.DriverProfile, name='driver_profile'),
    path('driver/profile-edit/', views.DriverEditor, name='driver_edit'),
    path('driver/register-error/', views.DriverRegisterErr, name='driver_register_error'),
    path('driver/ID-check/', views.DriverIDCheck, name='driver_check'),
    path('driver/search-request/', views.RideSearchingListView.as_view(), name='ride_search'),
    path('driver/ongoing-request-detail/<uuid:pk>/', views.CFRideDetail, name='cf_ride_detail'),
    path('driver/confirm-request/<uuid:pk>/', views.RideConfirm, name='ride_confirm'),
    path('owner/make-ride-request/', views.RideRequest, name='ride_request'),
    path('owner/ongoing-request-list/', views.CFRideStatusListView.as_view(), name='cf_ride_status'),
    
    
    path('owner/requests/', views.RequestListView.as_view(), name='requests'),   
    path('owner/request-detail/<uuid:pk>/', views.RequestDetail, name='cf_ride_request_check'),
    path('owner/requests/<uuid:pk>/', views.RideRequestEditing, name='ride_request_editing'),
    
    
    
    

    path('sharer/make-ride-request/', views.ShareRideRequest, name='share_ride_request'),
    path('sharer/ongoing-request-list/', views.ShareRequestListView.as_view(), name='share_requests'),
    path('sharer/request-detail/<uuid:pk>/', views.ShareRequestDetail, name='cf_share_ride_request_check'),
    path('sharer/available-ride-list/<uuid:pk>/', views.ShareRideSearchingListView.as_view(), name='share_ride_list'),
    path('sharer/join-ride/<uuid:main_id>/', views.JoinShareRide, name='middlepath'),
    path('sharer/join-ride/<uuid:main_id>/<uuid:share_id>/', views.JoinShareRide, name='share_ride_confirm'),
]
