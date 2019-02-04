from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home.html')


def loginHome(request):
    return render(request, 'loginhome.html')


def ownerHome(request):
    return render(request, 'ownerhome.html')


def driverHome(request):
    return render(request, 'driverhome.html')


def sharerHome(request):
    return render(request, 'sharerhome.html')


def successHome(request):
    return render(request, 'successhome.html')


def errorHome(request):
    return render(request, 'errorhome.html')
