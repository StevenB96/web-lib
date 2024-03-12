from django.db import models
from .base_model import BaseModel


class BookGenre(BaseModel):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.id}"

    class Meta:
        verbose_name_plural = 'Book Genres'
        db_table = 'book_genre'
        managed = True
