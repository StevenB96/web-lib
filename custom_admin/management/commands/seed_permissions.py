from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from ...model_classes import (
    Book,
    Author,
    Genre,
    ReadingList,
    ReadinglistBook,
    BookGenre,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # -------------------------- Auth groups
        auth_group_list = ['app_auth_group']

        for auth_group in auth_group_list:
            auth_group_record, created = Group.objects.get_or_create(
                name=auth_group
            )

            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Group for {auth_group} created"))
            else:
                self.stdout.write(self.style.WARNING(
                    f"Permission for {auth_group} already exists"))

        # -------------------------- Content types
        content_type_list = [
            Book,
            Author,
            Genre,
            ReadingList,
            ReadinglistBook,
            BookGenre,
        ]

        crud_operation_list = [
            'add',
            'change',
            'delete',
            'view',
        ]

        for content_type in content_type_list:
            content_type_record, created = ContentType.objects.get_or_create(
                app_label=content_type._meta.app_label,
                model=content_type._meta.model_name
            )

            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Content type for {content_type._meta.verbose_name_plural} created"))
            else:
                self.stdout.write(self.style.WARNING(
                    f"Content type for {content_type._meta.verbose_name_plural} already exists"))

            # -------------------------- Permissions
            for crud_operation in crud_operation_list:
                permission_record, created = Permission.objects.get_or_create(
                    content_type_id=content_type_record.id,
                    codename=f"{crud_operation}_{content_type_record.model}",
                    name=f"Can {crud_operation} {content_type_record.model}",
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Permission for {content_type._meta.verbose_name_plural} created"))

                    # -------------------------- Auth group permissions
                    app_auth_group = Group.objects.get(name='app_auth_group')
                    if not app_auth_group.permissions.filter(id=permission_record.id).exists():
                        app_auth_group.permissions.add(permission_record)
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Permission for {content_type._meta.verbose_name_plural} already exists"))
