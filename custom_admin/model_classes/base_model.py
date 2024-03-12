from django.db import models


class BaseModel(models.Model):
    STATUS_CHOICES = (
        (1, 'Inactive'),
        (2, 'Active'),
    )

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[1][0]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
