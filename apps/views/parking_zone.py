from http import HTTPStatus

from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView

from apps.models import ParkingZone
from apps.serialize import ParkingZoneModelSerializer
from auth_user.models import User


@extend_schema(tags=['zone'])
class ParkingZoneListAPIView(ListAPIView):
    queryset = ParkingZone.objects.all()
    serializer_class = ParkingZoneModelSerializer


@extend_schema(tags=['zone'])
class ParkingZoneRetrieveAPIView(RetrieveAPIView):
    queryset = ParkingZone.objects.all()
    serializer_class = ParkingZoneModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['zone'])
class ParkingZoneCreateAPIView(CreateAPIView):
    serializer_class = ParkingZoneModelSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role != User.RoleType.ADMIN:
            return JsonResponse({'message': 'user not admin'}, status=HTTPStatus.BAD_REQUEST)
        return super().create(request, *args, **kwargs)


@extend_schema(tags=['zone'])
class ParkingZoneUpdateAPIView(UpdateAPIView):
    queryset = ParkingZone.objects.all()
    serializer_class = ParkingZoneModelSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.role != User.RoleType.ADMIN:
            return JsonResponse({'message': 'user not admin'}, status=HTTPStatus.BAD_REQUEST)
        return super().update(request, *args, **kwargs)


@extend_schema(tags=['zone'])
class ParkingZoneDestroyAPIView(DestroyAPIView):
    queryset = ParkingZone.objects.all()
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.role != User.RoleType.ADMIN:
            return JsonResponse({'message': 'user not admin'}, status=HTTPStatus.BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)
