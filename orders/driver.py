from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DriverRegisterForm
from .models import Request, Driver, ShareRequest
from django.db import IntegrityError
from django.contrib import messages
from django.views import generic
from django.db.models import Q
from django.core.mail import EmailMessage


def RegisterErr(request):
    '''
    show the warning about repeat register as a driver
    '''
    messages.add_message(request, messages.INFO, "You have already registered as a driver")
    
    return redirect('home:loginHome')


@login_required
def OGINRequestIDcheck(request):
    try:
        Driver.objects.get(pk=request.user)
    except Driver.DoesNotExist:
        return redirect('orders:driver_register')
    return redirect('orders:driver_true_order_list')


class OGINRequestListView(LoginRequiredMixin, generic.ListView):
    '''
    Ride Satus Viewing
    List all the ongoing requests.
    '''
    mode = Request
    template_name = 'owner/OGIN_request_list.html'
    paginate_by = 10

    def get_queryset(self):
        driver = Driver.objects.get(pk=self.request.user)

        return Request.objects.filter(driver__exact=driver).filter(status__exact='cf')


@login_required

@login_required
def Register(request):
    '''
    Driver Registration
    User fill the register form to be a driver
    '''

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
            return redirect('home:successHome')

    else:
        form = DriverRegisterForm()
    return render(request, 'driver/register.html', {'form': form})


@login_required
def Profile(request):
    '''
    Driver info checking
    '''
    try:
        driver_info = Driver.objects.get(user=request.user)
    except Driver.DoesNotExist:
            return redirect('orders:driver_register')
    return render(request, 'driver/profile.html', {'driver_info': driver_info})


@login_required
def ProfileEditor(request):
    '''
    Driver Info Editing
    '''
    driver_info = get_object_or_404(Driver, user=request.user)
    if request.method == 'POST':
        form = DriverRegisterForm(request.POST)
        if form.is_valid():
            driver_info.first_name = form.cleaned_data['first_name']
            driver_info.last_name = form.cleaned_data['last_name']
            driver_info.type = form.cleaned_data['type']
            driver_info.plate_number = form.cleaned_data['plate_number']
            driver_info.max_passenger = form.cleaned_data['max_passenger']
            driver_info.special_car_info = form.cleaned_data['special_car_info']
            driver_info.save()
            return redirect('orders:driver_profile')

    else:
        first_name = driver_info.first_name
        last_name = driver_info.last_name
        type = driver_info.type
        plate_number = driver_info.plate_number
        max_passenger = driver_info.max_passenger
        special_car_info = driver_info.special_car_info
        form = DriverRegisterForm(initial={'first_name': first_name,
                                           'last_name': last_name,
                                           'type': type,
                                           'plate_number': plate_number,
                                           'max_passenger': max_passenger,
                                           'special_car_info': special_car_info,})
    context = {'form': form,
               'driver_info': driver_info}
    return render(request, 'driver/register.html', context)


@login_required
def ConfirmRequest(request, pk):
    '''
    Ride Searching(Driver)
    Drive confirms a request, owner, sharer, driver will receive an email notification
    '''
    request_detail = get_object_or_404(Request, pk=pk)
    driver = get_object_or_404(Driver, pk=request.user)
    share_request = ShareRequest.objects.filter(main_request=request_detail)
    request_detail.driver = driver
    request_detail.status = 'cf'
    request_detail.save()
    email = EmailMessage('Request Confirmed',
                         'Dear driver,\n\nYour request {} has been confirmed.\n\nBest,\nRide Share Service'.format(request_detail.id),
                         to=[driver.user.email])
    email.send()
    email = EmailMessage('Request Confirmed',
                         'Dear customor,\n\nYour request {} has been confirmed.\n\nBest,\nRide Share Service'.format(request_detail.id),
                         to=[request_detail.owner.email])
    email.send()
    for request in share_request:
        email = EmailMessage('Request Confirmed',
                             'Dear customor,\n\nYour request {} has been confirmed.\n\nBest,\nRide Share Service'.format(request_detail.id),
                             to=[request.sharer.email])
        email.send()
    return redirect('home:successHome')


@login_required
def OGINRideDetail(request, pk):
    '''
    Ride Status Viewing(Driver)
    Driver can mark a specific request to be completed
    '''
    try:
        Driver.objects.get(pk=request.user)
    except Driver.DoesNotExist:
        return redirect('orders:driver_register')
    ride_request = Request.objects.get(pk=pk)
    if ride_request.driver != request.driver:
        return redirect('home:errorHome')
    share_ride_request = ShareRequest.objects.filter(main_request=ride_request)
    if request.method == 'POST':
        ride_request.status = 'cp'
        ride_request.save()
        return redirect('home:successHome')
    return render(request, 'driver/OGINRideDetail.html',
                  {'ride_request': ride_request,
                   'share_ride_request': share_ride_request})


@login_required
def IDCheck(request):
    '''
    Check whether user has registered as a driver or not
    '''
    try:
        Driver.objects.get(pk=request.user)
    except Driver.DoesNotExist:
        return redirect('orders:driver_register')
    return redirect('home:driverHome')


@login_required
def SearchRequestIDcheck(request):
    try:
        Driver.objects.get(pk=request.user)
    except Driver.DoesNotExist:
        return redirect('orders:driver_register')
    return redirect('orders:driver_true_search_ride')


class SearchingRequestListView(LoginRequiredMixin, generic.ListView):
    '''
    Ride Searching(Driver)
    The Driver can search for open ride requests.
    '''
    mode = Request
    template_name = 'driver/op_request_list.html'
    paginate_by = 10

    def get_queryset(self):
        driver = Driver.objects.get(pk=self.request.user)
        return Request.objects.filter(status__exact='op').filter(total_passenger_num__lt=driver.max_passenger).filter(Q(type__exact=driver.type) | Q(type__isnull=True)).filter(special_car_info__exact=driver.special_car_info)
