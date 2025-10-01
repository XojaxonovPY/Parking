from http import HTTPStatus
from django.db.models import Sum, Count, Max
from django.http import JsonResponse
from django.views.generic import TemplateView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Payment, ParkingSpot, Reservation
from auth_user.models import User


@extend_schema(tags=['reports'])
class RevenueAPIView(APIView):
    def get(self, request):
        payment = Payment.objects.filter(status=Payment.PaymentStatus.SUCCESS).aggregate(
            total=Sum('amount'), count=Count('pk')
        )
        data = {
            'total_revenue': payment.get('total') or 0,
            'transaction_count': payment.get('count') or 0
        }
        return JsonResponse(data, status=HTTPStatus.OK)


@extend_schema(tags=['reports'])
class OccupancyAPIView(APIView):
    def get(self, request):
        data = {
            'available': ParkingSpot.objects.filter(status=ParkingSpot.Status.AVAILABLE).count(),
            'occupied': ParkingSpot.objects.filter(status=ParkingSpot.Status.OCCUPIED).count(),
            'reserved': ParkingSpot.objects.filter(status=ParkingSpot.Status.RESERVED).count(),
            'maintenance': ParkingSpot.objects.filter(status=ParkingSpot.Status.MAINTENANCE).count()
        }
        return JsonResponse(data, status=HTTPStatus.OK)


@extend_schema(tags=['reports'])
class UserActivAPIView(APIView):
    def get(self, request):
        user = request.user
        if user.role != User.RoleType.ADMIN:
            return JsonResponse({'message': 'user not admin'}, status=HTTPStatus.BAD_REQUEST)
        users = User.objects.all()
        data = []
        for user in users:
            reservations = Reservation.objects.filter(user=user)
            payment = Payment.objects.filter(user=user, status=Payment.PaymentStatus.SUCCESS)
            data.append({
                'user_id': user.pk ,
                'username': user.username or '',
                'reservations': reservations.count() or 0,
                'total_paid': payment.aggregate(total=Sum('amount')).get('total') or 0,
                'last_reservations': reservations.aggregate(last=Max('created_at')).get('last') or ''
            })
        return Response(data, status=HTTPStatus.OK)


