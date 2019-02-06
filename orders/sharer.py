from django.views import generic
from .forms import ShareRideRequestForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Request, Driver, ShareRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

@login_required
def MakeRequest(request):
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
    return render(request, 'sharer/make_request.html', {'form': form})


def RequestDetail(request, pk):
    '''
    Ride Satus Viewing(Sharer)
    Sharer can check the current ride details including
    driver and vehicle, and other sharer information
    '''
    share_ride_request = ShareRequest.objects.get(pk=pk)
    if share_ride_request.sharer != request.user:
        return redirect('home:errorHome')
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
        'pk': pk,
        }
    return render(request, 'sharer/request_detail.html', context)


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
    send_mail(
                'Joined Ride!',
                'Congratulation! You have successfully joined the ride.\n Your destination is: ' + share_ride_request.destination + ' Your arrival time is: ' + str(main_ride_request.arrival_time) + '.\n',
                'BatMobile',
                [request.user.email],
                fail_silently=False,
    )
    return redirect('home:loginHome')


class RequestListView(LoginRequiredMixin, generic.ListView):
    '''
    Ride Status Viewing(Sharer)
    display the list of all ongoing requests
    '''
    mode = ShareRequest
    template_name = 'sharer/request_list.html'
    paginate_by = 10

    def get_queryset(self):
        return ShareRequest.objects.all()

    def get_context_data(self, **kwargs):
        context = super(RequestListView, self).get_context_data(**kwargs)
        context['share_request_list'] = ShareRequest.objects.filter(sharer=self.request.user).exclude(main_request=None)
        return context

    
class AvailableRideSearchingListView(LoginRequiredMixin, generic.ListView):
    '''
    Ride Seaching(Sharer)
    The list of shared open rides
    '''
    mode = Request
    template_name = 'sharer/available_ride_list.html'
    paginate_by = 10

    def get_queryset(self):
        shareRequest = ShareRequest.objects.get(pk=self.kwargs['pk'])
        return Request.objects.filter(status__exact='op').filter(share_or_not__exact=True).filter(total_passenger_num__lt=(6-shareRequest.passenger_num)).filter(destination__exact=shareRequest.destination).filter(arrival_time__gte=shareRequest.early_arrival_time).filter(arrival_time__lte=shareRequest.late_arrival_time)

    def get_context_data(self, **kwargs):
        context = super(AvailableRideSearchingListView, self).get_context_data(**kwargs)
        context['share_request_id'] = self.kwargs['pk']
        return context


@login_required
def RideRequestEditing(request, pk):
    '''
    Ride Request Editing(Owner)
    User can edit the detail of this open request
    '''
    share_ride_request = get_object_or_404(ShareRequest, pk=pk)
    ride_request = share_ride_request.main_request
    if share_ride_request.sharer != request.user:
        return redirect('home:errorHome')
    if request.method == 'POST':
        form = ShareRideRequestForm(request.POST)
        if form.is_valid():
            ride_request.total_passenger_num -= share_ride_request.passenger_num
            share_ride_request.passenger_num = form.cleaned_data['passenger_num']
            ride_request.total_passenger_num += share_ride_request.passenger_num
            ride_request.save()
            share_ride_request.save()
            return redirect('home:successHome')
    else:
        form = ShareRideRequestForm(initial={'destination': share_ride_request.destination,
                                        'early_arrival_time': share_ride_request.early_arrival_time,
                                             'late_arrival_time': share_ride_request.late_arrival_time,
                                        'passenger_num': ride_request.passenger_num,})

    context = {
        'form': form,
        'share_ride_request': share_ride_request,
    }

    return render(request, 'sharer/share_ride_request_editing.html', context)

