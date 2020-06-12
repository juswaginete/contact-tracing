from users.views import UserProfileView

from django.conf.urls import url
from django.urls import include, path


urlpatterns = [
    path('', UserProfileView.as_view(), name="user_signup"),
]
