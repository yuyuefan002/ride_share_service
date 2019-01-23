from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required, permission_required
# from .models import Request, Driver
from django.contrib.auth.forms import UserCreationForm
from .forms import DriverRegisterForm, RideRequestForm
from django.contrib.auth.models import User
from .models import Request, Driver
from django.db import IntegrityError
from django.contrib import messages
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
    ride_request = Request.objects.create(owner=request.user)
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
        form = RideRequestForm()
    return render(request, 'ride_request.html', {'form': form})
