import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

optional = {
    'null': True,
    'blank': True,
}


class ServiceSchedule(models.Model):

    name = models.CharField(max_length=255, **optional)
    start_time = models.TimeField(default=datetime.time(8, 00))
    end_time = models.TimeField(default=datetime.time(17, 00))

    def __str__(self):
        return self.name


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )

    USER_TYPES = (
        (0, 'Staff'),
        (1, 'Admin'),
        (2, 'Church Member')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, **optional)
    address = models.CharField(max_length=255, **optional)
    birthday = models.DateField(default=timezone.now,)
    city = models.CharField(max_length=100, **optional)
    province = models.CharField(max_length=255, **optional)
    country = models.CharField(max_length=255, **optional)
    postal_code = models.PositiveIntegerField(**optional)
    phone_number = models.CharField(max_length=30, unique=True, **optional)
    user_type = models.IntegerField(choices=USER_TYPES, default=0)
    service_schedule = models.ForeignKey(
        ServiceSchedule,
        on_delete=models.CASCADE,
        related_name="user_schedule",
        **optional
    )

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
