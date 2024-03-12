from django.contrib import admin
from .base_admin import BaseAdmin

from ..model_classes import (
    Author,
)


class AuthorAdmin(BaseAdmin):
    fields = (
        'name',
        'status',
    )


admin.site.register(Author, AuthorAdmin)
