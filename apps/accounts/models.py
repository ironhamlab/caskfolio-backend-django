from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class ActiveUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    bio = models.CharField(max_length=150, blank=True)
    theme = models.CharField(max_length=10, default='light')
    note_default_public = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nickname']

    objects = ActiveUserManager()
    all_objects = UserManager()

    def __str__(self):
        return self.nickname