from .base_test import BaseTest
from ..model_classes import (
    BaseModel,
    Author
)


class AuthorTest(BaseTest):
    def test_load_author_page_authorised(self):
        self.client.force_login(self.test_user)

        response = self.client.get('/admin/custom_admin/author/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Authors')

    def test_load_author_page_unauthorised(self):
        self.client.force_login(self.unauthorised_user)

        response = self.client.get('/admin/custom_admin/author/')
        self.assertIn(response.status_code, [302, 403])

    def test_crud_author(self):
        self.client.force_login(self.test_user)

        # Add
        response = self.client.post('/admin/custom_admin/author/add/', {
            'name': 'Roald Dahl',
            'status': BaseModel.STATUS_CHOICES[1][0],
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        author = Author.objects.get(name='Roald Dahl')
        self.assertIsNotNone(author)

        # Update
        response = self.client.post(f'/admin/custom_admin/author/{author.id}/change/', {
            'name': 'William Shakespeare',
            'status': BaseModel.STATUS_CHOICES[1][0],
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        author.refresh_from_db()
        self.assertEqual(author.name, 'William Shakespeare')

        # Delete
        response = self.client.post(f'/admin/custom_admin/author/{author.id}/delete/', {
            'post': 'yes',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(name='William Shakespeare')
