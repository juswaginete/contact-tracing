from django.conf.urls import url
from django.urls import include, path

from users.views import ProfileUpdateView

urlpatterns = [
    path('<int:pk>/', ProfileUpdateView.as_view(), name="update_profile"),
]
