from auth_user.urls.login_reg import urlpatterns as main
from auth_user.urls.profile import urlpatterns as profile


urlpatterns=[
    *main,
    *profile
]