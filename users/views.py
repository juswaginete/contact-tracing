import datetime
import sys

from http import HTTPStatus

from django.contrib.auth import login as django_login, logout as django_logout
from django.utils import timezone

from rest_framework import (
    authentication,
    exceptions,
    parsers,
    renderers,
    status,
    viewsets,
    generics,
    mixins
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Profile
from users.serializers import (
    AuthCustomTokenSerializer,
    ProfileSerializer,
    UserProfileSerializer
)


class UserProfileView(APIView):
    """
    Handles api endpoints for user profile
    """

    def post(self, request):
        """
        Endpoint call for user registration
        """
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.process_create_user(request))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_current_datetime():
    return timezone.now().astimezone(timezone.get_default_timezone())


class ObtainAuthToken(APIView):
    """
    Handles api endpoint for logging in
    """

    def post(self, request, *args, **kwargs):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')

        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)

        if not created:
            user = token.user
            token.delete()
            token = Token.objects.create(user=user)
            token.created = get_current_datetime()
            token.save()

        return Response({
            'token': token.key
        }, status=200)


class LogoutView(APIView):
    """
    Handles api endpoint for logging out
    """

    def post(self, request, *args, **kwargs):
        """
        Hnadles in retrieving user token and deletes it afterwards
        """
        try:
            token = Token.objects.get(key=request.user.auth_token)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        token.delete()
        return Response(HTTPStatus.OK)


class UserProfileViewSet(viewsets.ViewSet):
    """
    Handles api endpoints for profiles list and details
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Display all profiles
        """
        profiles = Profile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieves user profiles from database
        """
        profile = Profile.objects.get(user__id=pk)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


class ProfileUpdateView(UpdateAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        try:
            user_profile = Profile.objects.get(user=request.user)
            if user_profile:

                user_profile.user.first_name = request.data.get('first_name', None)
                user_profile.user.last_name = request.data.get('last_name', None)
                user_profile.user.email = request.data.get('email', None)
                user_profile.user.username = request.data.get('username', None)
                user_profile.user.save()

                user_profile.city = request.data.get('city', None)
                user_profile.province = request.data.get('province', None)
                user_profile.address = request.data.get('address', None)
                user_profile.birthday = request.data.get('birthday', None)
                user_profile.gender = request.data.get('gender', None)
                user_profile.country_id = request.data.get('country', None)
                user_profile.save()

                return Response({
                    "user_id": user_profile.user.id,
                    "profile_id": user_profile.pk,
                    "first_name": user_profile.user.first_name,
                    "last_name": user_profile.user.last_name,
                    "email": user_profile.user.email,
                    "username": user_profile.user.username,
                    "city": user_profile.city,
                    "country": user_profile.country,
                    "province": user_profile.province,
                    "address": user_profile.address,
                    "birthday": user_profile.birthday,
                    "gender": user_profile.gender,
                    "phone_number": user_profile.phone_number,
                })

            else:
                return Response({
                    "error": True,
                    "status": 404,
                    "message": "Profile not found."
                })

        except Exception as e:
            return Response({
                "status": type(e).__name__,
                "traceback": 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno),
                "message": str(e)
            })
