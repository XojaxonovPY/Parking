from django.urls import path

from apps.views import *

urlpatterns = [
    path('save/payment/',PaymentCreateAPIView.as_view(),name='payment-save'),
    path('list/payment/',PaymentListAPIView.as_view(),name='payment-list'),
    path('detail/payment/<int:pk>',PaymentRetrieveAPIView.as_view(),name='payment-detail'),
    path('detail/payment/refund/<int:pk>',PaymentFailedAPIView.as_view(),name='payment-refund')

]