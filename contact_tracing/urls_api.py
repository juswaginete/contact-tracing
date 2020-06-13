from django.conf.urls import url
from django.urls import include, path

urlpatterns = [
    path('signup/', include('users.urls_signup')),
    path('login/', include('users.urls_login')),
    path('logout/', include('users.urls_logout')),
]
