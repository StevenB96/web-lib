from django.contrib import admin
from .base_admin import BaseAdmin

from ..model_classes import (
    Genre,
)


class GenreAdmin(BaseAdmin):
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


admin.site.register(Genre, GenreAdmin)
