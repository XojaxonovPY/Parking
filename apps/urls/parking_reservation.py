from django.urls import path

from apps.views import *

urlpatterns = [
    path('save/parking/reservation', ReservationCreateAPIView.as_view(), name='reservation-save'),
    path('list/parking/reservation', ReservationListAPIView.as_view(), name='reservation-list'),
    path('detail/parking/reservation/<int:pk>', ReservationRetrieveAPIView.as_view(), name='reservation-detail'),
    path('update/parking/reservation/<int:pk>', ReservationUpdateAPIView.as_view(), name='reservation-update'),
    path('delete/parking/reservation/<int:pk>', ReservationDestroyAPIView.as_view(), name='reservation-delete'),
    path('check/parking/reservation/<int:pk>', ReservationCheckApiView.as_view(), name='reservation-check'),
    path('check-out/parking/reservation/<int:pk>', ReservationCheckOutApiView.as_view(), name='reservation-check-out')
]
