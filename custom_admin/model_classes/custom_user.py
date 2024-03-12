from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Meta:
        verbose_name_plural = 'Users'
        db_table = 'custom_user'
        managed = True
