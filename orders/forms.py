
from django.forms import ModelForm
from .models import Driver
from django.core.exceptions import ValidationError
from django import forms


class DriverRegisterForm(ModelForm):

    def clean_max_passenger(self):
        data = self.cleaned_data['max_passenger']

        if data > 6 or data < 1:
            raise ValidationError('number is not in the correct range')
        return data

    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'type', 'plate_number', 'max_passenger', 'special_car_info']
        labels = {'type': 'Vehicle Type'}
        help_texts = {'max_passenger': 'Please input a number range from 1 to 6'}
