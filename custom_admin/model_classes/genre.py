from django.db import models
from .base_model import BaseModel
from .book_genre import BookGenre

class Genre(BaseModel):
    books = models.ManyToManyField('Book', through=BookGenre)
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f"{self.name} - {self.id}"

    class Meta:
        verbose_name_plural = 'Genres'
        db_table = 'genre'
        managed = True