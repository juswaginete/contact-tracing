from django.conf.urls import url
from django.urls import include, path

urlpatterns = [
    path('signup/', include('users.urls_signup')),
]
