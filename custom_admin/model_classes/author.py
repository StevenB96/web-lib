from django.db import models
from .base_model import BaseModel


class Author(BaseModel):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f"{self.name} - {self.id}"

    class Meta:
        verbose_name_plural = 'Authors'
        db_table = 'author'
        managed = True
