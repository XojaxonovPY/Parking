from http import HTTPStatus

from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Payment
from apps.serialize import PaymentModelSerializer
from auth_user.models import User


@extend_schema(tags=['payment'])
class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentModelSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


@extend_schema(tags=['payment'])
class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentModelSerializer


@extend_schema(tags=['payment'])
class PaymentRetrieveAPIView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['payment'], responses=PaymentModelSerializer)
class PaymentFailedAPIView(APIView):
    def put(self, request, pk):
        user = request.user
        if user.role != User.RoleType.ADMIN:
            return JsonResponse({'message': 'user not admin'}, status=HTTPStatus.BAD_REQUEST)
        payment = Payment.objects.filter(pk=pk)
        payment.update(status=Payment.PaymentStatus.FAILED)
        serialize = PaymentModelSerializer(instance=payment.first())
        return Response(serialize.data, HTTPStatus.OK)
