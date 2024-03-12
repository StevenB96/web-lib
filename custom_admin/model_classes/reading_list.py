from django.db import models
from .base_model import BaseModel
from .custom_user import CustomUser
from .readinglist_book import ReadinglistBook

class ReadingList(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    books = models.ManyToManyField('Book', through=ReadinglistBook, blank=True)
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f"{self.name} - {self.id}"

    class Meta:
        verbose_name_plural = 'Reading Lists'
        db_table = 'reading_list'
        managed = True