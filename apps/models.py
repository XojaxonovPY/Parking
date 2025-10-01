from django.db.models import Model, CharField, TextField, IntegerField, DecimalField, ForeignKey
from django.db.models import DateTimeField, TextChoices, CASCADE
from auth_user.models import User


class ParkingZone(Model):
    name = CharField(max_length=100)
    address = TextField()
    coordinates = CharField(max_length=255)
    total_spots = IntegerField()
    available_spots = IntegerField()
    hourly_rate = DecimalField(max_digits=8, decimal_places=2)
    daily_rate = DecimalField(max_digits=8, decimal_places=2)
    monthly_rate = DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class ParkingSpot(Model):
    class Status(TextChoices):
        AVAILABLE = 'available', 'Available'
        OCCUPIED = 'occupied', 'Occupied'
        RESERVED = 'reserved', 'Reserved'
        MAINTENANCE = 'maintenance', 'Maintenance'

    class SpotType(TextChoices):
        REGULAR = 'regular', 'Regular'
        HANDICAPPED = 'handicapped', 'Handicapped'
        ELECTRIC = 'electric', 'Electric'

    zone = ForeignKey(ParkingZone, on_delete=CASCADE, related_name='spots')
    spot_number = CharField(max_length=50)
    status = CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    spot_type = CharField(max_length=20, choices=SpotType.choices, default=SpotType.REGULAR)

    def __str__(self):
        return f"{self.zone.name} - {self.spot_number}"


class Reservation(Model):
    class Status(TextChoices):
        PENDING = 'pending', 'Pending'
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = ForeignKey(User, on_delete=CASCADE,related_name='reservations')
    spot = ForeignKey(ParkingSpot, on_delete=CASCADE,related_name='reservations')
    start_time = DateTimeField()
    end_time = DateTimeField()
    status = CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total_amount = DecimalField(max_digits=10, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.spot}"


class Payment(Model):
    class PaymentMethod(TextChoices):
        CARD = 'card', 'Card'
        CASH = 'cash', 'Cash'
        WALLET = 'wallet', 'Wallet'
        OTHER = 'other', 'Other'

    class PaymentStatus(TextChoices):
        SUCCESS = 'success', 'Success'
        PENDING = 'pending', 'Pending'
        FAILED = 'failed', 'Failed'

    reservation = ForeignKey(Reservation, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    amount = DecimalField(max_digits=10, decimal_places=2)
    payment_method = CharField(max_length=20, choices=PaymentMethod.choices)
    status = CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    transaction_id = CharField(max_length=255, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.status}"

