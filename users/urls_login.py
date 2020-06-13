from users.views import ObtainAuthToken

from django.conf.urls import url
from django.urls import include, path


urlpatterns = [
    path('', ObtainAuthToken.as_view(), name="login_user")
]
