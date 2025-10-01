from django.urls import path

from apps.views import RevenueAPIView, OccupancyAPIView, UserActivAPIView

urlpatterns = [
    path('get/revenue/', RevenueAPIView.as_view(), name='revenue'),
    path('get/occupancy/', OccupancyAPIView.as_view(), name='occupancy'),
    path('get/user/activate/', UserActivAPIView.as_view(), name='user-active'),

]
