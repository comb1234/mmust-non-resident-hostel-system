from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    registration_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    course = models.CharField(max_length=100, blank=True)
    year_of_study = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username