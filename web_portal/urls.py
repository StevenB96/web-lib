from django.urls import path
from .views import (
    LoginView,
    RegistrationView,
    LogoutView,
    HomeView,
    BooksView,
    ReadingListBooksView,
)

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path(
        'registration/',
        RegistrationView.as_view(),
        name='registration'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
    path(
        'home/',
        HomeView.as_view(),
        name='home'
    ),
    path(
        'reading_list/<int:reading_list_id>/<str:operation>',
        BooksView.as_view(),
        name='reading_list'
    ),
    path(
        'readinglist_book/<int:reading_list_id>/<int:book_id>/<str:operation>',
        ReadingListBooksView.as_view(),
        name='readinglist_book'
    ),
]
