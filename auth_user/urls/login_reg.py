from django.urls import path
from auth_user.views.login_reg import *

urlpatterns = [
    path('login/', CustomerTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomerTokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    path('register/', register_api_view),
    path('check-email/', email_check_api_view),
    path('forgot/password/', forgot_password_ap_view),
]
