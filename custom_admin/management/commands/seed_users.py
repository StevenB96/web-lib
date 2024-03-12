from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from custom_admin.model_classes import (
    CustomUser,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # -------------------------- Users
        initial_user_list = [
            {
                'username': 'admin_user',
                'email': 'admin_user@example.com',
                'password': 'adminpass',
                'is_superuser': True,
                'is_staff': True,
                'is_active': True,
            },
            {
                'username': 'staff_user',
                'email': 'staff_user@example.com',
                'password': 'staffpass',
                'is_superuser': False,
                'is_staff': True,
                'is_active': True,
                'auth_group_list': [
                    Group.objects.get(name='app_auth_group')
                ],
            },
            {
                'username': 'app_user',
                'email': 'app_user@example.com',
                'password': 'apppass',
                'is_superuser': False,
                'is_staff': False,
                'is_active': True,
            },
        ]

        user_model_fields = [
            field.name for field in CustomUser._meta.get_fields()]

        for user in initial_user_list:
            user_data = {key: value for key,
                         value in user.items() if key in user_model_fields}
            username = user_data["username"]
            if not CustomUser.objects.filter(username=username).exists():
                user_record = CustomUser.objects.create_user(**user_data)
                if user_record:
                    self.stdout.write(self.style.SUCCESS(
                        f"User ({username}) created"))

                    # -------------------------- User auth groups
                    if 'auth_group_list' in user:
                        for auth_group in user['auth_group_list']:
                            if not user_record.groups.filter(id=auth_group.id).exists():
                                user_record.groups.add(auth_group)
                else:
                    self.stdout.write(self.style.WARNING(
                        f"User ({username}) creation failed"))

            else:
                self.stdout.write(self.style.WARNING(
                    f"User ({username}) already exists"))
