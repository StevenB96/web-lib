from django.db import models
from .base_model import BaseModel
from .author import Author
from .book_genre import BookGenre
from .readinglist_book import ReadinglistBook


class Book(BaseModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genres = models.ManyToManyField('Genre', through=BookGenre, blank=True)
    reading_lists = models.ManyToManyField('ReadingList', through=ReadinglistBook)
    title = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.FloatField()
    published_date = models.DateTimeField()

    def __str__(self):
        return f"{self.title} - {self.id}"

    class Meta:
        verbose_name_plural = 'Books'
        db_table = 'book'
        managed = True
