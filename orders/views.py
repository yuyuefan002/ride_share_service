from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from .models import Request, Driver
from django.contrib.auth.forms import UserCreationForm
from .forms import DriverRegisterForm, RideRequestForm
from django.contrib.auth.models import User
from .models import Request, Driver
from django.db import IntegrityError
from django.contrib import messages
from django.views import generic
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


class RequestListView(LoginRequiredMixin, generic.ListView):
    mode = Request
    template_name = 'request_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Request.objects.filter(owner__exact=self.request.user).exclude(status__exact='cp')


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
        destination=ride_request.destination
        arrival_time=ride_request.arrival_time
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
