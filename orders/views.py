from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from .models import Request, Driver
from django.contrib.auth.forms import UserCreationForm
from .forms import DriverRegisterForm, RideRequestForm, ShareRideRequestForm
from django.contrib.auth.models import User
from .models import Request, Driver, ShareRequest
from django.db import IntegrityError
from django.contrib import messages
from django.views import generic
from django.db.models import Q
from django.core.mail import EmailMessage
# Create your views here.


@login_required
def index(request):
    return render(request, 'index.html')


def DriverRegisterErr(request):
    messages.add_message(request, messages.INFO, "You have already registered as a driver")
    
    return redirect('orders:index')

@login_required
def DriverRegister(request):
    if request.method == 'POST':
        form = DriverRegisterForm(request.POST)
        if form.is_valid():
            try:
                driver_info = Driver.objects.create(user=request.user, max_passenger=1)
            except IntegrityError:
                return redirect('orders:driver_register_error')
            driver_info.first_name = form.cleaned_data['first_name']
            driver_info.last_name = form.cleaned_data['last_name']
            driver_info.type = form.cleaned_data['type']
            driver_info.plate_number = form.cleaned_data['plate_number']
            driver_info.max_passenger = form.cleaned_data['max_passenger']
            driver_info.special_car_info = form.cleaned_data['special_car_info']
            driver_info.save()
            return redirect('orders:index')

    else:
        form = DriverRegisterForm()
    return render(request, 'driver_register.html', {'form': form})


@login_required
def RideRequest(request):
    if request.method == 'POST':
        form = RideRequestForm(request.POST)
        if form.is_valid():
            ride_request = Request.objects.create(owner=request.user)
            ride_request.destination = form.cleaned_data['destination']
            ride_request.arrival_time = form.cleaned_data['arrival_time']
            ride_request.passenger_num = form.cleaned_data['passenger_num']
            ride_request.share_or_not = form.cleaned_data['share_or_not']
            ride_request.type = form.cleaned_data['type']
            ride_request.special_car_info = form.cleaned_data['special_car_info']
            ride_request.remarks = form.cleaned_data['remarks']
            ride_request.save()            
            return redirect('orders:index')
    else:
        form = RideRequestForm()
    return render(request, 'ride_request.html', {'form': form})


@login_required
def ShareRideRequest(request):
    if request.method == 'POST':
        form = ShareRideRequestForm(request.POST)
        if form.is_valid():
            share_ride_request = ShareRequest.objects.create(sharer=request.user)
            share_ride_request.destination = form.cleaned_data['destination']
            share_ride_request.early_arrival_time = form.cleaned_data['early_arrival_time']
            share_ride_request.late_arrival_time = form.cleaned_data['late_arrival_time']
            share_ride_request.passenger_num = form.cleaned_data['passenger_num']
            share_ride_request.save()
            return redirect('orders:share_ride_list', pk=share_ride_request.id)
    else:
        form = ShareRideRequestForm()
    return render(request, 'share_ride_request.html', {'form': form})


def CFRideRequestCheck(request,pk):
    ride_request = get_object_or_404(Request, pk=pk)
    driver_info = get_object_or_404(Driver, pk=ride_request.driver.user)
    context = {
        'driver_info': driver_info,
        'ride_request': ride_request,
    }

    '''
    {'create_date': ride_request.create_date,
          'status': ride_request.status,
          'driver': driver_info.user,
          'vehicle_type': driver_info.type,
          'vehicle_plate_num': driver_info.plate_number,
          'destination': ride_request.destination,
          'passenger_num': ride_request.passenger_num,
          'special_car_info': ride_request.special_car_info,
          'remarks': ride_request.remarks,
    }
    '''
    return render(request, "cf_ride_request_check.html", context)


def RideRequestJump(request, pk):
    ride_request = get_object_or_404(Request, pk=pk)
    if ride_request.status == 'op':
        return redirect('orders:ride_request_editing', pk=ride_request.id)
    return redirect('orders:cf_ride_request_check', pk=ride_request.id)


def RideRequestEditing(request, pk):
    ride_request = get_object_or_404(Request, pk=pk)
    if request.method == 'POST':
        form = RideRequestForm(request.POST)
        if form.is_valid():
            ride_request.destination = form.cleaned_data['destination']
            ride_request.arrival_time = form.cleaned_data['arrival_time']
            ride_request.passenger_num = form.cleaned_data['passenger_num']
            ride_request.share_or_not = form.cleaned_data['share_or_not']
            ride_request.type = form.cleaned_data['type']
            ride_request.special_car_info = form.cleaned_data['special_car_info']
            ride_request.remarks = form.cleaned_data['remarks']
            ride_request.save()
            return redirect('orders:index')
    else:
        destination = ride_request.destination
        arrival_time = ride_request.arrival_time
        passenger_num = ride_request.passenger_num
        share_or_not = ride_request.share_or_not
        type = ride_request.type
        special_car_info = ride_request.special_car_info
        remarks = ride_request.remarks
        form = RideRequestForm(initial={'destination': destination,
                                        'arrival_time': arrival_time,
                                        'passenger_num': passenger_num,
                                        'share_or_not': share_or_not,
                                        'type':type,
                                        'special_car_info': special_car_info,
                                        'remarks': remarks})
    context = {
        'form': form,
        'ride_request': ride_request,
    }

    return render(request, 'ride_request_editing.html', context)

@login_required
def DriverCheck(request):
    try:
        Driver.objects.get(pk=request.user)
    except Driver.DoesNotExist:
        return redirect('orders:driver_register')
    return redirect('orders:ride_search')

@login_required
def RideConfirm(request, pk):
    request_detail = get_object_or_404(Request, pk=pk)
    driver = get_object_or_404(Driver, pk=request.user)
    request_detail.driver = driver
    request_detail.status = 'cf'
    request_detail.save()
    email = EmailMessage('Request Confirmed', 'Dear driver,\n\nYour request {} has been confirmed.\n\nBest,\nRide Share Service'.format(request_detail.id), to=[driver.user.email])
    email.send()
    email = EmailMessage('Request Confirmed', 'Dear customor,\n\nYour request {} has been confirmed.\n\nBest,\nRide Share Service'.format(request_detail.id), to=[request_detail.owner.email])
    email.send()
    return redirect('orders:index')

@login_required
def ShareRideConfirm(request, main_id):
    return redirect('orders:index')


class RequestListView(LoginRequiredMixin, generic.ListView):
    mode = Request
    template_name = 'request_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Request.objects.filter(owner__exact=self.request.user).exclude(status__exact='cp')
    

class RideSearchingListView(LoginRequiredMixin, generic.ListView):
    mode = Request
    template_name = 'op_request_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        driver = Driver.objects.get(pk=self.request.user)
        return Request.objects.filter(status__exact='op').filter(passenger_num__lt=driver.max_passenger).filter(Q(type__exact=driver.type) | Q(type__isnull=True)).filter(special_car_info__icontains=driver.special_car_info)


class ShareRideSearchingListView(LoginRequiredMixin, generic.ListView):
    mode = Request
    template_name = 'share_ride_list.html'
    paginate_by = 10

    def get_queryset(self):
        shareRequest = ShareRequest.objects.get(pk=self.kwargs['pk'])
        return Request.objects.filter(status__exact='op').filter(share_or_not__exact=True).filter(passenger_num__lt=(6-shareRequest.passenger_num))
