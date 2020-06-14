from django.contrib import admin
from django.contrib.auth.models import User

from users.models import Profile, ServiceSchedule


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'gender',
        'phone_number',
    )

    search_fields = (
        'user__first_name',
        'user__last_name',
        'phone_number'
    )


class ServiceScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'start_time',
        'end_time',
    )

    search_fields = (
        'name',
    )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ServiceSchedule, ServiceScheduleAdmin)
