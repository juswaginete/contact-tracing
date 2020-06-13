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
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response

from users.serializers import ProfileSerializer, AuthCustomTokenSerializer


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
            'id': user.id,
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }, status=200)


class LogoutView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(key=request.user.auth_token)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        token.delete()
        return Response(HTTPStatus.OK)
