from django.test import TestCase, Client
from ..model_classes import CustomUser

class BaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.test_user, created = CustomUser.objects.get_or_create(
            username='test_user',
            email='test_user@example.com',
            password='test_password',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        
        cls.unauthorised_user, created = CustomUser.objects.get_or_create(
            username='unauthorised_user',
            email='unauthorised_user@example.com',
            password='unauthorised_password',
            is_staff=True,
            is_active=True,
        )

    def setUp(self):
        super().setUp()
        self.client = Client()

    def tearDown(self):
        self.client.logout()
        super().tearDown()
