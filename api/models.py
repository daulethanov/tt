import random
import string
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models as m


class UserManager(BaseUserManager):
    def create_user(self, numbers, password=None):
        if not numbers:
            raise ValueError('The numbers must be set')

        user = self.model(numbers=numbers)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, numbers, password=None):
        user = self.create_user(numbers, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    numbers = m.CharField(max_length=12, unique=True)
    code = m.CharField(max_length=6, unique=True)
    invite_profile = m.CharField(max_length=6, null=True, blank=True)
    username = m.CharField(max_length=12)
    is_staff = m.BooleanField(default=True)
    USERNAME_FIELD = 'numbers'

    objects = UserManager()

    def generate_code(self):
        characters = string.ascii_letters.lower() + string.digits
        code = ''.join(random.choice(characters) for _ in range(6))
        self.code = code

    def __str__(self):
        return self.numbers





