import sys
import re

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

from users.models import Profile


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


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class fro User Profiling with UniqueValidators
    """
    user = UserModelSerializer(required=True)
    phone_number = serializers.CharField(
        max_length=15,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )

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
            )
            user_profile.save()

            return {
                "user": user.id,
                "phone_number": phone_number,
                "gender": gender,
                "birthday": birthday,
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
        )
