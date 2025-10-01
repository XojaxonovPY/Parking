from django.contrib import admin
from apps.models import ParkingZone, Payment, ParkingSpot, Reservation


@admin.register(ParkingZone)
class ParkingZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'total_spots', 'available_spots')
    search_fields = ('name', 'address')
    ordering = ('name',)

@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ('spot_number', 'zone', 'status', 'spot_type')
    list_filter = ('status', 'spot_type', 'zone')
    search_fields = ('spot_number',)
    ordering = ('zone', 'spot_number')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'spot', 'start_time', 'end_time', 'status', 'total_amount')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'spot__spot_number')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'reservation', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('user__username', 'transaction_id')
    readonly_fields = ('transaction_id', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

