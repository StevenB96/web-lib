from django.contrib import admin
from .base_admin import BaseAdmin

from ..model_classes import (
    Genre,
)


class GenreAdmin(BaseAdmin):
    fields = (
        'name',
        'status',
    )


admin.site.register(Genre, GenreAdmin)
