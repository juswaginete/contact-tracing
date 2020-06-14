import sys
import re

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import exceptions
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
import django.contrib.auth.password_validation as validators

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.settings import settings
from rest_framework.validators import UniqueValidator

from users.models import Profile, ServiceSchedule


class UserModelSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate(self, data):
        user = User(**data)
        password =  data.get('password')
        errors = dict()

        try:
            validators.validate_password(password=password, user=User)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserModelSerializer, self).validate(data)

    class Meta:
        model = User
        fields = ('first_name', 'username', 'last_name', 'email', 'password')


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class fro User Profiling with UniqueValidators
    """
    user = UserModelSerializer(required=True)
    phone_number = serializers.CharField(
        max_length=15,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
    service_schedule = serializers.IntegerField()

    def process_create_user(self, request):
        try:
            user = self.data.get('user')
            email = user.get('email')
            username = user.get('username')
            first_name = user.get('first_name')
            last_name = user.get('last_name')
            password = user.get('password')
            phone_number = self.data.get('phone_number')
            birthday = self.data.get('birthday')
            gender = self.data.get('gender')
            user_type = self.data.get('user_type')
            service_schedule = ServiceSchedule.objects.get(id=self.data.get('service_schedule'))

            user = User(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            user.set_password(password)
            user.save()

            user_profile = Profile(
                user=user,
                phone_number=phone_number,
                birthday=birthday,
                gender=gender,
                user_type=user_type,
                service_schedule=service_schedule,
            )
            user_profile.save()

            return {
                "user": user.id,
                "phone_number": phone_number,
                "gender": gender,
                "birthday": birthday,
                "user_type": user_type,
            }
        except Exception as e:
            return {
                "status": type(e).__name__,
                "traceback": 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno),
                "message": str(e)
            }

    class Meta:
        model = Profile
        fields = (
            "user",
            "phone_number",
            "birthday",
            "gender",
            "user_type",
            "service_schedule",
        )


class AuthCustomTokenSerializer(serializers.Serializer):
    """
    Serializer class for authenticating user credentials
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            try:
                validate_email(username)

                user_request = get_object_or_404(User, email=username)
                username = user_request.username
            except ValidationError as e:
                try:
                    user_request = get_object_or_404(
                        Profile, phone_number=username)
                    username = user_request.user.username
                except ValidationError as e:
                    return Response({
                        "status": 400,
                        "error": True,
                        "message": str(e),
                    })
            user = authenticate(username=username, password=password)
        else:
            msg = _('Must include email/phone number and a password.')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs
