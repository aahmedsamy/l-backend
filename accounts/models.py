from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


# Create your models here.


class User(AbstractUser):
    email = models.EmailField('email address', unique=True, )

    """User model."""
    use_in_migrations = True

    REQUIRED_FIELDS = ['email', ]
    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
