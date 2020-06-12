from django.contrib import admin
from django.contrib.auth.models import User

from users.models import Profile


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


admin.site.register(Profile, ProfileAdmin)
