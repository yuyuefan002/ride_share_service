
from django.contrib import admin
from .models import Request, Driver
# Register your models here.


class DriverInline(admin.TabularInline):
    model = Driver
    extra = 0


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    # list_display = ['id', 'owner', 'driver', 'create_date', 'destination', 'arrival_time', 'passenger_num', 'share_or_not', 'special_car_info', 'remarks', 'status']
    list_display = ['id', 'create_date', 'owner','status']
    list_filter = ('status', 'passenger_num')
    fieldsets = ((None, {'fields': ('id', 'create_date', 'status', 'share_or_not',)}),
                 ('Passenger info', {'fields': ('owner', 'destination', 'arrival_time', 'passenger_num')}),
                 ('Vehicle info', {'fields': ('type', 'special_car_info', 'remarks')}))
    inlines = [DriverInline]


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'user', 'type', 'plate_number', 'max_passenger', 'special_car_info']
