from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # You can add custom fields like phone number, etc.
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    # Any other custom fields can be added here

    def __str__(self):
        return self.username
