from apps.urls.parking_zone import urlpatterns as parking_zone
from apps.urls.parking_spots import urlpatterns as parking_spots
from apps.urls.parking_reservation import urlpatterns as parking_reservation
from apps.urls.payment import urlpatterns as payment
from apps.urls.reports import urlpatterns as reports

urlpatterns = [
    *parking_zone,
    *parking_spots,
    *parking_reservation,
    *payment,
    *reports
]
