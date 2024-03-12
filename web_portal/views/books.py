from django.views import View
from django.utils.html import format_html
import django_tables2 as tables
from django.db.models import Value, IntegerField, Value, OuterRef, Exists, F
from django.shortcuts import render, redirect
from ..helpers import CustomLoginRequiredMixin
from custom_admin.model_classes import (
    ReadingList,
    Book,
)


class BookTable(tables.Table):
    title = tables.Column(
        order_by=('title',),
        verbose_name="Title"
    )
    description = tables.Column(
        order_by=('description',),
        verbose_name="Description"
    )
    rating = tables.Column(
        order_by=('rating',),
        verbose_name="Rating"
    )
    author = tables.Column(
        order_by=('author',),
        verbose_name="Author"
    )
    genres = tables.Column(
        verbose_name="Genres",
        orderable=False,
    )
    toggle = tables.TemplateColumn(
        "<div style='width: 100%; display: flex; justify-content: center;'><a style='text-decoration: none;' href='{% url 'readinglist_book' record.reading_list_id record.id 'toggle' %}'>{% if record.book_in_reading_list %}➖{% else %}➕{% endif %}</a></div>",
        orderable=False,
        verbose_name="Toggle"
    )

    class Meta:
        model = Book
        fields = ('title', 'description', 'rating', 'author',)
        attrs = {'class': 'book-table'}

    def render_genres(self, record):
        genres = record.genres.all()
        genre_names = ', '.join(genre.name for genre in genres)

        return genre_names
    
    def render_description(self, value):
        max_length = 300
        if len(value) > max_length:
            truncated_value = value[:max_length] + '...'
            return format_html('<span title="{}">{}</span>', value, truncated_value)
        else:
            return value


class BooksView(CustomLoginRequiredMixin, View):
    def get_queryset(self, reading_list_id):
        queryset = Book.objects.all()

        # Annotate each book with the reading_list_id
        queryset = Book.objects.annotate(
            reading_list_id=Value(reading_list_id, output_field=IntegerField())
        )

        # Subquery to check if the book is in the reading list
        book_in_reading_list_subquery = ReadingList.objects.filter(
            # Use the annotated reading_list_id
            id=OuterRef('reading_list_id'),
            # OuterRef refers to the primary key of the Book model
            books=OuterRef('pk')
        ).values('id')

        # Annotate each book with a boolean indicating if it's in the reading list
        queryset = queryset.annotate(
            book_in_reading_list=Exists(book_in_reading_list_subquery)
        )

        # Order the queryset based on whether the book is in the reading list
        queryset = queryset.order_by(
            F('book_in_reading_list').desc(),
            'title'
        )

        # Filter the queryset
        if self.request.GET.get('title_filter'):
            queryset = queryset.filter(
                title__icontains=self.request.GET.get('title_filter'))
        elif self.request.GET.get('description_filter'):
            queryset = queryset.filter(
                description__icontains=self.request.GET.get('description_filter'))
        elif self.request.GET.get('rating_filter'):
            rating_filter = self.request.GET.get('rating_filter')
            queryset = queryset.filter(rating__startswith=str(rating_filter))
        elif self.request.GET.get('author_filter'):
            queryset = queryset.filter(
                author__name__icontains=self.request.GET.get('author_filter'))
        elif self.request.GET.get('genre_filter'):
            queryset = queryset.filter(
                genres__name__icontains=self.request.GET.get('genre_filter')).distinct()

        # Order the queryset based on the sort parameter
        sort = self.request.GET.get('sort')
        if sort == 'title':
            queryset = queryset.order_by('title')
        elif sort == 'description':
            queryset = queryset.order_by('description')
        elif sort == 'rating':
            queryset = queryset.order_by('rating')            
        elif sort == 'author':
            queryset = queryset.order_by('author')

        return queryset

    def get_table(self, queryset):
        table = BookTable(queryset)
        return table

    def get(self, request, reading_list_id, operation):
        if (operation == 'delete'):
            reading_list = ReadingList.objects.get(id=reading_list_id)
            reading_list.delete()
            redirect_url = request.META.get('HTTP_REFERER')
            if redirect_url:
                return redirect(redirect_url)

        queryset = self.get_queryset(reading_list_id)
        table = self.get_table(queryset)

        return render(request, "books.html", {
            "table": table,
            "filters": [
                {
                    'name': 'title',
                    'label': 'Title',
                    'type': 'text',
                },
                {
                    'name': 'description',
                    'label': 'Description',
                    'type': 'text',
                },
                {
                    'name': 'rating',
                    'label': 'Rating',
                    'type': 'number',
                },
                {
                    'name': 'author',
                    'label': 'Author',
                    'type': 'text',
                },
                {
                    'name': 'genre',
                    'label': 'Genre',
                    'type': 'text',
                },
            ],
            "filter_direction": "row",
        })
