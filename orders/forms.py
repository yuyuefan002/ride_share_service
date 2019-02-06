from django.forms import ModelForm
from bootstrap_datepicker_plus import DateTimePickerInput
from .models import Request, ShareRequest, Driver
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class DriverRegisterForm(ModelForm):
    class Meta:
        model = Driver
        fields =['first_name','last_name','type','plate_number','max_passenger','special_car_info',]
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'type': 'Car type',
            'plate_number': 'Plate Number',
            'max_passenger': 'How many people can you have?',
            'special_car_info': 'Any special Info about your car?',
        }

    
class RideRequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['destination', 'arrival_time', 'passenger_num', 'share_or_not', 'type', 'special_car_info', 'remarks']
        labels = {'arrival_time': 'Requested Arrival Time', 'passenger_num': 'How many people do you have?',
                  'share_or_not': 'Do you want to share your ride?',
                  'special_car_info': 'Any special car request?'}
        widgets = {
            'arrival_time': DateTimePickerInput()
        }

        
class ShareRideRequestForm(ModelForm):
    class Meta:
        model = ShareRequest
        fields = ['destination', 'early_arrival_time',
                  'late_arrival_time', 'passenger_num', ]
        labels = {'early_arrival_time': 'Earliest Arrival Time',
                  'late_arrival_time': 'Latest Arrival Time',
                  'passenger_num': 'How many people do you have?', }
        widgets = {
            'early_arrival_time': DateTimePickerInput(),
            'late_arrival_time': DateTimePickerInput(),
        }



