from django.contrib.auth.models import BaseUserManager

import datetime


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, username, email, **extra_fields):
        """Create and save a User with the given phone and password."""
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(extra_fields['password'])
        user.save(using=self._db)
        return user

    def create_user(self, username, email,  **extra_fields):
        """Create and save a regular User with the given phone and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, **extra_fields)

    def create_superuser(self, username, email, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')


        return self._create_user(username, email, **extra_fields)