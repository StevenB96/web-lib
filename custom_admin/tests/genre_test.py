from .base_test import BaseTest
from ..model_classes import (
    BaseModel,
    Genre
)


class GenreTest(BaseTest):
    def test_load_genre_page_authorised(self):
        self.client.force_login(self.test_user)

        response = self.client.get('/admin/custom_admin/genre/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Genres')

    def test_load_genre_page_unauthorised(self):
        self.client.force_login(self.unauthorised_user)

        response = self.client.get('/admin/custom_admin/genre/')
        self.assertIn(response.status_code, [302, 403])

    def test_crud_genre(self):
        self.client.force_login(self.test_user)

        # Add
        response = self.client.post('/admin/custom_admin/genre/add/', {
            'name': 'Fiction',
            'status': BaseModel.STATUS_CHOICES[1][0],
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        genre = Genre.objects.get(name='Fiction')
        self.assertIsNotNone(genre)

        # Update
        response = self.client.post(f'/admin/custom_admin/genre/{genre.id}/change/', {
            'name': 'Non-fiction',
            'status': BaseModel.STATUS_CHOICES[1][0],
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        genre.refresh_from_db()
        self.assertEqual(genre.name, 'Non-fiction')

        # Delete
        response = self.client.post(f'/admin/custom_admin/genre/{genre.id}/delete/', {
            'post': 'yes',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Genre.DoesNotExist):
            Genre.objects.get(name='Non-fiction')
