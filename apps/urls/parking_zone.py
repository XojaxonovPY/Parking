from django.urls import path

from apps.views import *

urlpatterns = [
    path('get/parking/zone',ParkingZoneListAPIView.as_view(),name='zone_list'),
    path('save/parking/zone',ParkingZoneCreateAPIView.as_view(),name='zone_save'),
    path('update/parking/zone/<int:pk>',ParkingZoneUpdateAPIView.as_view(),name='zone_update'),
    path('delete/parking/zone/<int:pk>',ParkingZoneDestroyAPIView.as_view(),name='zone_delete'),
    path('detail/parking/zone/<int:pk>',ParkingZoneRetrieveAPIView.as_view(),name='zone_detail')
]