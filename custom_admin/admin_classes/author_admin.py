from django.contrib import admin
from .base_admin import BaseAdmin

from ..model_classes import (
    Author,
)


class AuthorAdmin(BaseAdmin):
    search_fields  = [
        'name',
    ]

    list_display  = [
        "name",
        'status',
    ]
    
    fields = (
        'name',
        'status',
    )

    ordering = (
        'name',
        'status',
    )


admin.site.register(Author, AuthorAdmin)
