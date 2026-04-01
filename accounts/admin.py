from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('bio', 'avatar', 'favourite_genre')}),
    )
    list_display = ('username', 'email', 'is_staff', 'date_joined')