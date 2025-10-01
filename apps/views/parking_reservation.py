from http import HTTPStatus

from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Reservation
from apps.serialize import ReservationModelSerializer


@extend_schema(tags=['reservation'])
class ReservationCreateAPIView(CreateAPIView):
    serializer_class = ReservationModelSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


@extend_schema(tags=['reservation'])
class ReservationListAPIView(ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationModelSerializer

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(user=self.request.user)
        return query


@extend_schema(tags=['reservation'])
class ReservationRetrieveAPIView(RetrieveAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['reservation'])
class ReservationUpdateAPIView(UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['reservation'])
class ReservationDestroyAPIView(DestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['reservation'], responses=ReservationModelSerializer)
class ReservationCheckApiView(APIView):
    def put(self, request, pk):
        reservations = Reservation.objects.filter(pk=pk)
        reservations.update(status=Reservation.Status.ACTIVE)
        serialize = ReservationModelSerializer(instance=reservations.first())
        return Response(serialize.data, HTTPStatus.OK)


@extend_schema(tags=['reservation'], responses=ReservationModelSerializer)
class ReservationCheckOutApiView(APIView):
    def put(self, request, pk):
        reservations = Reservation.objects.filter(pk=pk)
        reservations.update(status=Reservation.Status.COMPLETED)
        serialize = ReservationModelSerializer(instance=reservations.first())
        return Response(serialize.data, HTTPStatus.OK)
