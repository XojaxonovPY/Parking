from http import HTTPStatus
from django.db.models import Q
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import ParkingSpot
from apps.serialize import ParkingSpotModelSerializer
from auth_user.models import User


@extend_schema(tags=['spot'])
class ParkingSpotListAPIView(ListAPIView):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotModelSerializer


@extend_schema(tags=['spot'])
class SpotAvailableListAPIView(ListAPIView):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotModelSerializer

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(status=ParkingSpot.Status.AVAILABLE)
        return query


@extend_schema(tags=['spot'])
class ParkingSpotCreateAPIView(CreateAPIView):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotModelSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role != User.RoleType.ADMIN:
            return JsonResponse({'message': 'user is not admin'}, status=HTTPStatus.BAD_REQUEST)
        return super().create(request, *args, **kwargs)


@extend_schema(tags=['spot'])
class ParkingSpotUpdateAPIView(UpdateAPIView):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotModelSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.role != User.RoleType.ADMIN:
            return JsonResponse({'message': 'user is not admin'}, status=HTTPStatus.BAD_REQUEST)
        return super().update(request, *args, **kwargs)


@extend_schema(tags=['spot'], parameters=[
    OpenApiParameter(name='status', required=True, type=str, enum=ParkingSpot.Status.values, description='chose status')
], responses=ParkingSpotModelSerializer)
class ParkingSpotAPIView(APIView):
    def get(self, request, pk):
        status = request.query_params.get('status')
        parking = ParkingSpot.objects.filter(Q(pk=pk) & Q(status=status)).first()
        serialize = ParkingSpotModelSerializer(instance=parking)
        return Response(serialize.data, status=HTTPStatus.OK)
