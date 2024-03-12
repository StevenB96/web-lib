from .base_test import BaseTest
from ..model_classes import (
    ReadingList,
    BaseModel
)


class ReadingListTest(BaseTest):
    def test_load_reading_list_page_authenticated(self):
        self.client.force_login(self.test_user)

        response = self.client.get('/admin/custom_admin/readinglist/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reading List')

    def test_load_reading_list_page_unauthenticated(self):
        self.client.force_login(self.unauthorised_user)

        response = self.client.get('/admin/custom_admin/readinglist/')
        self.assertIn(response.status_code, [302, 403])

    def test_crud_reading_list_item(self):
        self.client.force_login(self.test_user)

        # Add
        response = self.client.post('/admin/custom_admin/readinglist/add/', {
            'user': self.test_user.id,
            'name': 'Summer Reads',
            'status': BaseModel.STATUS_CHOICES[1][0],
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        reading_list = ReadingList.objects.get(name='Summer Reads')
        self.assertIsNotNone(reading_list)

        # Update
        response = self.client.post(f'/admin/custom_admin/readinglist/{reading_list.id}/change/', {
            'user': self.test_user.id,
            'name': 'Winter Reads',
            'status': BaseModel.STATUS_CHOICES[1][0],
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        reading_list.refresh_from_db()
        self.assertEqual(reading_list.name, 'Winter Reads')

        # Delete
        response = self.client.post(f'/admin/custom_admin/readinglist/{reading_list.id}/delete/', {
            'confirm_delete': 'yes',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ReadingList.DoesNotExist):
            ReadingList.objects.get(name='Winter Reads')
