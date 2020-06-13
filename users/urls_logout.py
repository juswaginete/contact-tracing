from users.views import LogoutView

from django.conf.urls import url
from django.urls import include, path


urlpatterns = [
    path('', LogoutView.as_view(), name="logout_user")
]
