from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from custom_users.models import User


@admin.register(User)
class Admin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'token')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'email_key')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
