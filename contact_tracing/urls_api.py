from django.conf.urls import url
from django.urls import include, path

from rest_framework.routers import SimpleRouter

from users.views import UserProfileViewSet

profile_router = SimpleRouter()
profile_router.register(r'', UserProfileViewSet, basename='profile-list')

urlpatterns = [
    path('signup/', include('users.urls_signup')),
    path('login/', include('users.urls_login')),
    path('logout/', include('users.urls_logout')),
    path('profiles/', include(profile_router.urls)),
]
