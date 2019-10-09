from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


# Create your models here.


class User(AbstractUser):
    MALE = "Male"
    FEMALE = "Female"
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female")
    )
    email = models.EmailField('email address', unique=True, )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    """User model."""
    use_in_migrations = True

    REQUIRED_FIELDS = ['email', ]
    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Lover(models.Model):
    male = models.OneToOneField(User, on_delete=models.PROTECT, unique=True, related_name="male_user")
    female = models.OneToOneField(User, on_delete=models.PROTECT, unique=True, related_name="female_user")

    def __str__(self):
        return f"{self.male.first_name} - {self.female.first_name}"