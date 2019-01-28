from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DriverRegisterForm, RideRequestForm, ShareRideRequestForm
from .models import Request, Driver, ShareRequest
from django.db import IntegrityError
from django.contrib import messages
from django.views import generic
from django.db.models import Q
from django.core.mail import EmailMessage
# Create your views here.


@login_required
def index(request):
    '''
    main page
    '''
    return render(request, 'index.html')


def DriverRegisterErr(request):
    '''
    show the warning about repeat register as a driver
    '''
    messages.add_message(request, messages.INFO, "You have already registered as a driver")
    
    return redirect('orders:index')


@login_required
def DriverRegister(request):
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
            return redirect('orders:index')

    else:
        form = DriverRegisterForm()
    return render(request, 'driver_register.html', {'form': form})


@login_required
def DriverProfile(request):
    '''
    Driver info checking
    '''
    driver_info = Driver.objects.get(user=request.user)
    return render(request, 'driver_check.html', {'driver_info': driver_info})


@login_required
def DriverEditor(request):
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
    return render(request, 'driver_register.html', context)


@login_required
def RideRequest(request):
    '''
    Ride Requesting
    User can request a ride by filling in this form
    '''
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
            ride_request.total_passenger_num = ride_request.passenger_num
            ride_request.save()  
            return redirect('orders:index')
    else:
        form = RideRequestForm()
    return render(request, 'ride_request.html', {'form': form})


@login_required
def ShareRideRequest(request):
    '''
    Ride Searching(Sharer)
    Sharer can fillin the form to generate their order, and use the information
    to look up the available ride
    '''
    if request.method == 'POST':
        form = ShareRideRequestForm(request.POST)
        if form.is_valid():
            try:
                share_ride_request = ShareRequest.objects.get(main_request=None)
                share_ride_request.sharer = request.user
            except ShareRequest.DoesNotExist:
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


def RequestDetail(request, pk):
    '''
    Ride Status Viewing(Owner)
    Owner can check the current ride details including
    driver and vehicle, sharer information
    '''
    ride_request = get_object_or_404(Request, pk=pk)
    if ride_request.driver is not None:
        driver_info = Driver.objects.get(pk=ride_request.driver.user)
    else:
        driver_info = None
    try:
        share_ride_request = ShareRequest.objects.filter(main_request=ride_request.id)
    except ShareRequest.DoesNotExist:
        share_ride_request = None
    context = {
        'driver_info': driver_info,
        'ride_request': ride_request,
        'share_ride_request': share_ride_request,
        'pk': pk,
    }
    return render(request, "request_detail.html", context)


def ShareRequestDetail(request, pk):
    '''
    Ride Satus Viewing(Sharer)
    Sharer can check the current ride details including
    driver and vehicle, and other sharer information
    '''
    share_ride_request = ShareRequest.objects.get(pk=pk)
    ride_request = share_ride_request.main_request
    try:
        driver_info = Driver.objects.get(pk=share_ride_request.main_request.driver)
        driver_info = Driver.objects.get(pk=share_ride_request.
                                         main_request.driver)
    except Driver.DoesNotExist:
        driver_info = None
    try:
        share_ride_request = ShareRequest.objects.filter(main_request=ride_request.id)
    except ShareRequest.DoesNotExist:
        share_ride_request = None
    context = {
            'share_ride_request': share_ride_request,
            'ride_request': ride_request,
            'driver_info': driver_info,
        }
    return render(request, 'request_detail.html', context)


def RideRequestJump(request, pk):
    '''
    Ride Request Editing/Viewing Jump(Owner)
    Jump based on the status of request
    '''
    ride_request = get_object_or_404(Request, pk=pk)
    if ride_request.status == 'op':
        return redirect('orders:ride_request_editing', pk=ride_request.id)
    return redirect('orders:cf_ride_request_check', pk=ride_request.id)


def RideRequestEditing(request, pk):
    '''
    Ride Request Editing(Owner)
    User can edit the detail of this open request
    '''
    ride_request = get_object_or_404(Request, pk=pk)
    if request.method == 'POST':
        form = RideRequestForm(request.POST)
        if form.is_valid():
            ride_request.total_passenger_num -= ride_request.passenger_num
            ride_request.destination = form.cleaned_data['destination']
            ride_request.arrival_time = form.cleaned_data['arrival_time']
            ride_request.passenger_num = form.cleaned_data['passenger_num']
            ride_request.total_passenger_num += ride_request.passenger_num
            ride_request.share_or_not = form.cleaned_data['share_or_not']
            ride_request.type = form.cleaned_data['type']
            ride_request.special_car_info = form.cleaned_data['special_car_info']
            ride_request.remarks = form.cleaned_data['remarks']
            ride_request.save()
            return redirect('orders:cf_ride_request_check', pk=pk)
    else:
        form = RideRequestForm(initial={'destination': ride_request.destination,
                                        'arrival_time': ride_request.arrival_time,
                                        'passenger_num': ride_request.passenger_num,
                                        'share_or_not': ride_request.share_or_not,
                                        'type': ride_request.type,
                                        'special_car_info': ride_request.special_car_info,
                                        'remarks': ride_request.remarks})
    context = {
        'form': form,
        'ride_request': ride_request,
    }

    return render(request, 'ride_request_editing.html', context)


@login_required
def CFRideDetail(request, pk):
    '''
    Ride Status Viewing(Driver)
    Driver can mark a specific request to be completed
    '''
    ride_request = Request.objects.get(pk=pk)
    share_ride_request = ShareRequest.objects.filter(main_request=ride_request)
    if request.method == 'POST':
        ride_request.status = 'cp'
        ride_request.save()
        return redirect('orders:index')
    return render(request, 'cf_ride_detail.html',
                  {'ride_request': ride_request,
                   'share_ride_request': share_ride_request})


@login_required
def DriverIDCheck(request):
    '''
    Check whether user has registered as a driver or not
    '''
    try:
        Driver.objects.get(pk=request.user)
    except Driver.DoesNotExist:
        return redirect('orders:driver_register')
    return redirect('orders:ride_search')


@login_required
def RideConfirm(request, pk):
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
    return redirect('orders:index')


@login_required
def JoinShareRide(request, main_id, share_id):
    '''
    Ride Searching(Sharer)
    Sharer can join a selected open ride
    '''
    share_ride_request = ShareRequest.objects.get(pk=share_id)
    main_ride_request = Request.objects.get(pk=main_id)
    main_ride_request.total_passenger_num += share_ride_request.passenger_num
    share_ride_request.main_request = main_ride_request
    main_ride_request.save()
    share_ride_request.save()
    return redirect('orders:index')


class RequestListView(LoginRequiredMixin, generic.ListView):
    '''
    Ride Status Viewing(Owner)
    display the list of all ongoing requests
    '''
    mode = Request
    template_name = 'request_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Request.objects.filter(owner__exact=self.request.user).exclude(status__exact='cp')


class ShareRequestListView(LoginRequiredMixin, generic.ListView):
    '''
    Ride Status Viewing(Sharer)
    display the list of all ongoing requests
    '''
    mode = ShareRequest
    template_name = 'share_request_list.html'
    paginate_by = 10

    def get_queryset(self):
        return ShareRequest.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ShareRequestListView, self).get_context_data(**kwargs)
        context['share_request_list'] = ShareRequest.objects.filter(sharer=self.request.user).exclude(main_request=None)
        return context

    
class RideSearchingListView(LoginRequiredMixin, generic.ListView):
    '''
    Ride Searching(Driver)
    The Driver can search for open ride requests.
    '''
    mode = Request
    template_name = 'op_request_list.html'
    paginate_by = 10

    def get_queryset(self):
        driver = Driver.objects.get(pk=self.request.user)
        return Request.objects.filter(status__exact='op').filter(total_passenger_num__lt=driver.max_passenger).filter(Q(type__exact=driver.type) | Q(type__isnull=True)).filter(special_car_info__exact=driver.special_car_info)


class CFRideStatusListView(LoginRequiredMixin, generic.ListView):
    '''
    Ride Satus Viewing
    List all the ongoing requests.
    '''
    mode = Request
    template_name = 'cf_request_list.html'
    paginate_by = 10

    def get_queryset(self):
        driver = Driver.objects.get(pk=self.request.user)
        return Request.objects.filter(driver__exact=driver).filter(status__exact='cf')


class ShareRideSearchingListView(LoginRequiredMixin, generic.ListView):
    '''
    Ride Seaching(Sharer)
    The list of shared open rides
    '''
    mode = Request
    template_name = 'share_ride_list.html'
    paginate_by = 10

    def get_queryset(self):
        shareRequest = ShareRequest.objects.get(pk=self.kwargs['pk'])
        return Request.objects.filter(status__exact='op').filter(share_or_not__exact=True).filter(total_passenger_num__lt=(6-shareRequest.passenger_num)).filter(destination__exact=shareRequest.destination).filter(arrival_time__gte=shareRequest.early_arrival_time).filter(arrival_time__lte=shareRequest.late_arrival_time)

    def get_context_data(self, **kwargs):
        context = super(ShareRideSearchingListView, self).get_context_data(**kwargs)
        context['share_request_id'] = self.kwargs['pk']
        return context
