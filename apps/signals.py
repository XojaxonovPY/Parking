from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.models import Reservation, ParkingSpot, Payment


@receiver(post_save, sender=Reservation)
def update_spot_status_on_reservation(sender, instance, created, **kwargs):
    if created:
        instance.spot.status = ParkingSpot.Status.RESERVED
        instance.spot.save()


@receiver(post_delete, sender=Reservation)
def free_spot_on_reservation_delete(sender, instance, **kwargs):
    instance.spot.status = ParkingSpot.Status.AVAILABLE
    instance.spot.save()


@receiver(post_save, sender=Payment)
def update_reservation_status_on_payment(sender, instance, **kwargs):
    if instance.status == Payment.PaymentStatus.SUCCESS:
        instance.reservation.status = Reservation.Status.ACTIVE
        instance.reservation.save()
