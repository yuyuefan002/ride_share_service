from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Driver, Request
from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class DriverRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    VEHICLE_TYPE = (
        ('sd', 'sedan'),
        ('sv', 'SUV'),
        ('vn', 'van'),
        ('lx', 'Luxury'),
    )
    
    type = forms.ChoiceField(
        choices=VEHICLE_TYPE,
        initial='sd',
        help_text='vehicle type',
        )
    plate_number = forms.CharField(max_length=20)
    max_passenger = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], initial=1)
    special_car_info = forms.CharField(required=False,  max_length=1000, )
    help_texts = {'special_car_info':'special car infos'}

    
class RideRequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['destination', 'arrival_time', 'passenger_num', 'share_or_not', 'type', 'special_car_info', 'remarks']
        labels = {'arrival_time': 'Requested Arrival Time', 'passenger_num': 'How many people do you have?',
                  'share_or_not': 'Do you want to share your ride?',
                  'special_car_info': 'Any special car request?'}
        # widget = {'arrival_time': SplitDateTimeWidget() }
