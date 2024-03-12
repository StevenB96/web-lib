from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ..model_classes import (
    CustomUser,
)


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password'
            )
        }
        ),
        (
            'Personal info', {
                'fields': (
                    'first_name',
                    'last_name'
                )
            }
        ),
        (
            'Permissions', {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions'
                )
            }
        ),
        (
            'Important dates',
            {
                'fields': (
                    'last_login',
                    'date_joined'
                )
            }
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': (
                'wide',
            ),
            'fields': (
                'email',
                'password1',
                'password2'
            ),
        }),
    )
    list_display = (
        'username',
        'email',
        'first_name',
        'is_staff'
    )
    search_fields = (
        'username',
        'email',
    )
    ordering = (
        'username',
        'email',
        'first_name',
        'is_staff'
    )


admin.site.register(CustomUser, CustomUserAdmin)
