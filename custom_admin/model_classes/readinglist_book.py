from django.db import models
from .base_model import BaseModel


class ReadinglistBook(BaseModel):
    reading_list = models.ForeignKey('ReadingList', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} - {self.id}"

    class Meta:
        verbose_name_plural = 'Reading List Book'
        db_table = 'readinglist_book'
        managed = True
