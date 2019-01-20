from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
# from .models import Request, Driver
from django.contrib.auth.forms import UserCreationForm
from .forms import DriverRegisterForm
from django.contrib.auth.models import User
# Create your views here.


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def DriverRegister(request):
    if request.method == 'POST':
        form = DriverRegisterForm(request.POST)
        if form.is_valid():
            # form.Meta.model.user = request.user
            form.save()
            return redirect('orders:index')

    else:
        form = DriverRegisterForm()
    return render(request, 'driver_register.html', {'form': form})

