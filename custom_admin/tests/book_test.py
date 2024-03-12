from .base_test import BaseTest
from ..model_classes import (
    BaseModel,
    Book,
    Author
)


class BookTest(BaseTest):
    def test_load_book_page_authorised(self):
        self.client.force_login(self.test_user)

        response = self.client.get('/admin/custom_admin/book/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Books')

    def test_load_book_page_unauthorised(self):
        self.client.force_login(self.unauthorised_user)

        response = self.client.get('/admin/custom_admin/book/')
        self.assertIn(response.status_code, [302, 403])

    def test_crud_book(self):
        self.client.force_login(self.test_user)

        author = Author.objects.create(
            name='William Shakespeare',
            status=BaseModel.STATUS_CHOICES[1][0],
        )

        response = self.client.post('/admin/custom_admin/book/add/', {
            'author': author.id,
            'title': 'Hamlet',
            'description': "Depicts Prince Hamlet and his attempts to exact revenge against his uncle, Claudius, who has murdered Hamlet's father in order to seize his throne.",
            'rating': 1,
            'published_date_0': '1599-01-01',
            'published_date_1': '12:00:00',
            'status': BaseModel.STATUS_CHOICES[1][0],
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        book = Book.objects.get(title='Hamlet')
        self.assertIsNotNone(book)

        # Update
        response = self.client.post(f'/admin/custom_admin/book/{book.id}/change/', {
            'author': author.id,
            'title': 'The Tragedy of Hamlet',
            'description': "One of the most powerful and influential tragedies in the English language.",
            'rating': 2,
            'published_date_0': '1601-01-01',
            'published_date_1': '12:00:00',
            'status': BaseModel.STATUS_CHOICES[1][0],
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        book.refresh_from_db()
        self.assertEqual(book.title, 'The Tragedy of Hamlet')

        # Delete
        response = self.client.post(f'/admin/custom_admin/book/{book.id}/delete/', {
            'post': 'yes',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(title='The Tragedy of Hamlet')
