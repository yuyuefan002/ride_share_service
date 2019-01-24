from django.db import models
from django.contrib.auth.models import User
import uuid
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


# Create your models here.
class Driver(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    VEHICLE_TYPE = (
        ('sd', 'sedan'),
        ('sv', 'SUV'),
        ('vn', 'van'),
        ('lx', 'Luxury'),
    )
    type = models.CharField(
        max_length=2,
        choices=VEHICLE_TYPE,
        blank=True,
        default='sd',
        help_text='vehicle type',
        null=False)
    plate_number = models.CharField(max_length=20,null=False)
    max_passenger = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)],null=False)
    special_car_info = models.TextField('special_car_info', null=True, blank=True, max_length=1000)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('order:driver-info',args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular request')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # sharer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True,blank=True)
    create_date = models.DateTimeField('Creation Date', default=timezone.now)
    destination = models.CharField(max_length=200)
    arrival_time = models.DateTimeField(null=True, blank=True)
    passenger_num = models.IntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(6)])
    share_or_not = models.BooleanField(default=False)
    VEHICLE_TYPE = (
        ('sd', 'sedan'),
        ('sv', 'SUV'),
        ('vn', 'van'),
        ('lx', 'Luxury'),
    )
    type = models.CharField(
        max_length=2,
        choices=VEHICLE_TYPE,
        null=True,
        blank=True,
        help_text='optional, vehicle type')
    special_car_info = models.TextField('special_car_info', null=True, blank=True, max_length=1000)
    remarks = models.TextField('remarks', null=True, blank=True, max_length=1000)
    REQUEST_STATUS = (
        ('op', 'open'),
        ('cf', 'Confirmed'),
        ('cp', 'Complete'),
    )
    status = models.CharField(
        max_length=2,
        choices=REQUEST_STATUS,
        blank=True,
        default='op',
        help_text='Request Status',
    )

    class Meta:
        ordering = ['create_date', 'owner']

    def __str__(self):
        return f'{self.create_date}: {self.id} {self.owner}'

    def get_absolute_url(self):
        return reverse('orders:ride_request_editing', args=[str(self.id)])

    def get_confirm_url(self):
        return reverse('orders:ride_confirm', args=[str(self.id)])

