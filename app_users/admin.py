from django.contrib import admin
from app_users.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

    class Meta:
        model = Profile
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

admin.site.register(Profile, ProfileAdmin)