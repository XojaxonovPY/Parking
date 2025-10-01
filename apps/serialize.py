from rest_framework.serializers import ModelSerializer

from apps.models import ParkingZone, ParkingSpot, Reservation, Payment


class ParkingZoneModelSerializer(ModelSerializer):
    class Meta:
        model = ParkingZone
        fields = ('name', 'address', 'available_spots', 'coordinates', 'daily_rate', 'hourly_rate', 'monthly_rate',
                  'total_spots')



class ParkingSpotModelSerializer(ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields=('zone','spot_type','spot_number','status')


class ReservationModelSerializer(ModelSerializer):
    class Meta:
        model=Reservation
        fields=('user','spot','start_time','end_time','total_amount','status')
        read_only_fields=('user','status')


class PaymentModelSerializer(ModelSerializer):
    class Meta:
        model=Payment
        fields=('reservation','amount','payment_method','status','user','created_at')
        read_only_fields = ('user', 'status','created_at')

