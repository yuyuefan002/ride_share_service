from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RideRequestForm
from .models import Request, Driver, ShareRequest
from django.views import generic
from django.core.mail import send_mail

@login_required
def MakeRequest(request):
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
            send_mail(
                'Request confirmed!',
                'Congratulation! You have successfully made a request.\n Destination is: ' + form.cleaned_data['destination'] + ' Arrival time is: ' + str(form.cleaned_data['arrival_time']) + '.\n',
                'BatMobile',
                [request.user.email],
                fail_silently=False,
            )

            return redirect('home:successHome')
    else:
        form = RideRequestForm()
    return render(request, 'owner/make_request.html', {'form': form})



class RequestListView(LoginRequiredMixin, generic.ListView):
    '''
    Ride Status Viewing(Owner)
    display the list of all ongoing requests
    '''
    mode = Request
    template_name = 'owner/request_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Request.objects.filter(owner__exact=self.request.user).exclude(status__exact='cp')

    
def RequestDetail(request, pk):
    '''
    Ride Status Viewing(Owner)
    Owner can check the current ride details including
    driver and vehicle, sharer information
    '''
    ride_request = get_object_or_404(Request, pk=pk)
    if ride_request.owner != request.user:
        return redirect('home:errorHome')
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
    return render(request, "owner/request_detail.html", context)

@login_required
def RideRequestEditing(request, pk):
    '''
    Ride Request Editing(Owner)
    User can edit the detail of this open request
    '''
    ride_request = get_object_or_404(Request, pk=pk)
    if ride_request.owner != request.user:
        return redirect('home:errorHome')
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

    return render(request, 'owner/ride_request_editing.html', context)

