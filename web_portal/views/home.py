from django.views import View
import django_tables2 as tables
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from custom_admin.model_classes import (
    ReadingList,
    BaseModel,
    Book,
)


class HomeTable(tables.Table):
    name = tables.Column(
        order_by=('name',),
        verbose_name="Name"
    )
    books = tables.Column(
        orderable=False,
        verbose_name="Books"
    )
    view = tables.TemplateColumn(
        "<div style='width: 100%; display: flex; justify-content: center;'><a style='text-decoration: none;' href='{% url 'reading_list' record.id 'view' %}'>🔍</a></div>",
        orderable=False,
        verbose_name="View"
    )
    delete = tables.TemplateColumn(
        "<div style='width: 100%; display: flex; justify-content: center;'><a style='text-decoration: none;' href='{% url 'reading_list' record.id 'delete' %}'>🗑️</a></div>",
        orderable=False,
        verbose_name="Delete"
    )

    class Meta:
        model = ReadingList
        fields = ('name', 'books',)
        attrs = {'class': 'home-table'}

    def render_books(self, record):
        books = record.books.all()
        book_names = ', '.join(book.title for book in books)

        return book_names


class HomeView(LoginRequiredMixin, View):
    def get_queryset(self):
        logged_in_user = self.request.user
        queryset = ReadingList.objects.filter(user=logged_in_user)

        name_filter = self.request.GET.get('name_filter')
        book_filter = self.request.GET.get('book_filter')

        # Filter the queryset
        if name_filter:
            queryset = queryset.filter(name__icontains=name_filter)
        elif book_filter:
            queryset = queryset.filter(book__title__icontains=book_filter)

        # Order the queryset based on the sort parameter
        sort = self.request.GET.get('sort')
        if sort == 'name':
            queryset = queryset.order_by('name')

        return queryset

    def get_table(self, queryset):
        table = HomeTable(queryset)
        return table

    def get(self, request):
        queryset = self.get_queryset()
        table = self.get_table(queryset)

        return render(request, "home.html", {
            "table": table,
            "filters": [
                {
                    'name': 'name',
                    'label': 'Name',
                    'type': 'text',
                },
                {
                    'name': 'book',
                    'label': 'Book',
                    'type': 'text',
                },
            ],
            "filter_direction": "column",
        })

    def post(self, request):
        # Create Reading List
        if 'name' in request.POST:
            name = request.POST['name']
            logged_in_user = request.user
            reading_list = ReadingList.objects.create(
                user=logged_in_user,
                name=name,
                status=BaseModel.STATUS_CHOICES[1][0]
            )

        redirect_url = request.META.get('HTTP_REFERER')
        if redirect_url:
            return redirect(redirect_url)


class ReadingListBooksView(LoginRequiredMixin, View):
    def get(self, request, reading_list_id, book_id, operation):
        if (operation == 'toggle'):
            reading_list = ReadingList.objects.get(id=reading_list_id)
            book = Book.objects.get(id=book_id)

            # Check if the book is already in the reading list
            if reading_list.books.filter(id=book_id).exists():
                reading_list.books.remove(book)
            else:
                reading_list.books.add(book)

            redirect_url = request.META.get('HTTP_REFERER')
            if redirect_url:
                return redirect(redirect_url)
