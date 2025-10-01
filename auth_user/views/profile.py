from http import HTTPStatus

from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from auth_user.models import User
from auth_user.serialize import UserModelSerializer


@extend_schema(responses=UserModelSerializer, tags=['profile'])
@api_view(['GET'])
def get_user_api_view(request):
    user = UserModelSerializer(request.user)
    return Response(user.data, status=HTTPStatus.OK)


@extend_schema(request=UserModelSerializer, responses=UserModelSerializer, tags=['profile'])
@api_view(['PUT'])
def update_user_api_view(request):
    user = User.objects.filter(pk=request.user.pk)
    user.update(**request.data)
    serialize = UserModelSerializer(instance=user, many=True)
    return Response(serialize.data, status=HTTPStatus.OK)


@extend_schema(responses=UserModelSerializer, tags=['profile'])
@api_view(['GET'])
def get_all_user_api_view(request):
    user = request.user
    if User.RoleType.ADMIN == user.role:
        obj = User.objects.all()
        serialize = UserModelSerializer(instance=obj, many=True)
        return Response(serialize.data, status=HTTPStatus.OK)
    return JsonResponse({'message': 'your not admin'}, status=HTTPStatus.BAD_REQUEST)


@extend_schema(tags=['profile'])
@api_view(['DELETE'])
def delete_user_api_view(request, pk):
    user = request.user
    if User.RoleType.ADMIN == user.role:
        User.objects.filter(pk=pk).delete()
        return JsonResponse({'message': 'user is deleted'}, status=HTTPStatus.OK)
    return JsonResponse({'message': 'your not admin'}, status=HTTPStatus.BAD_REQUEST)
