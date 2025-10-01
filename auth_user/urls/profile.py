from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from auth_user.views.profile import *





urlpatterns=[
    path('get/user',get_user_api_view),
    path('update/user',update_user_api_view),
    path('get/all/users',get_all_user_api_view),
    path('delete/users/<int:pk>',delete_user_api_view),
]
