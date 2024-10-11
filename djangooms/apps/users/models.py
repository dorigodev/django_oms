from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class StoreUserManager(BaseUserManager):
    def create_user(self, username, email, cnpj, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username.strip(), email=email, cnpj=cnpj, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, cnpj, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, cnpj, password, **extra_fields)


class StoreUser(AbstractUser):
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(unique=True, max_length=254)
    cnpj = models.CharField(unique=True, max_length=14)

    objects = StoreUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'cnpj']

    def __str__(self):
        return self.username
