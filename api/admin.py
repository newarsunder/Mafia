from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('color', 'room', 'host', 'joined_at')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('username', 'password', 'color')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Room)
