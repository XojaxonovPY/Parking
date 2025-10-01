from django.urls import path

from apps.views import *

urlpatterns = [
    path('get/parking/spot', ParkingSpotListAPIView.as_view(), name='spot-list'),
    path('get/parking/spot/avalibale', SpotAvailableListAPIView.as_view(), name='spot-available'),
    path('save/parking/spot/', ParkingSpotCreateAPIView.as_view(), name='spot-save'),
    path('update/parking/spot/<int:pk>', ParkingSpotUpdateAPIView.as_view(), name='spot-update'),
    path('detail/parking/spot/<int:pk>', ParkingSpotAPIView.as_view(), name='spot-detail')
]
