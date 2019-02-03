from django.urls import path
from .import views, driver, owner, sharer

app_name = 'orders'
urlpatterns =[
    path('', views.index, name='index'),
    path('driver/register/', driver.Register, name='driver_register'),
    path('driver/profile/', driver.Profile, name='driver_profile'),
    path('driver/profile-edit/', driver.ProfileEditor, name='driver_edit'),
    path('driver/register-error/', driver.RegisterErr, name='driver_register_error'),
    path('driver/ID-check/', driver.IDCheck, name='driver_check'),
    path('driver/search-request-IDcheck/', driver.SearchRequestIDcheck, name='driver_search_ride'),
    path('driver/search-request', driver.SearchingRequestListView.as_view(), name='driver_true_search_ride'),
    path('driver/ongoing-request-detail/<uuid:pk>/', driver.OGINRideDetail, name='cf_ride_detail'),
    path('driver/confirm-request/<uuid:pk>/', driver.ConfirmRequest, name='ride_confirm'),
    path('driver/ongoing-request-list-IDcheck/',driver.OGINRequestIDcheck, name='driver_order_list'),
    path('driver/ongoing-request-list/', driver.OGINRequestListView.as_view(), name='driver_true_order_list'),

    
    path('owner/make-ride-request/', owner.MakeRequest, name='owner_request_ride'),
    path('owner/requests/', owner.RequestListView.as_view(), name='owner_order_list'),   
    path('owner/request-detail/<uuid:pk>/', owner.RequestDetail, name='cf_ride_request_check'),
    path('owner/requests/<uuid:pk>/', owner.RideRequestEditing, name='ride_request_editing'),
    
    
    
    

    path('sharer/make-ride-request/', sharer.MakeRequest, name='sharer_request_ride'),
    path('sharer/ongoing-request-list/', sharer.RequestListView.as_view(), name='sharer_order_list'),
    path('sharer/request-detail/<uuid:pk>/', sharer.RequestDetail, name='cf_share_ride_request_check'),
    path('sharer/available-ride-list/<uuid:pk>/', sharer.AvailableRideSearchingListView.as_view(), name='share_ride_list'),
    path('sharer/join-ride/<uuid:main_id>/', sharer.JoinShareRide, name='middlepath'),
    path('sharer/join-ride/<uuid:main_id>/<uuid:share_id>/', sharer.JoinShareRide, name='share_ride_confirm'),
]
