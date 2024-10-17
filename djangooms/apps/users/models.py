from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager

# Create your models here.

class SupplierUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError("Users must have a password")
        email = self.normalize_email(email)
        user = self.model(username=username.strip(), email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class SupplierUser(AbstractUser):
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(unique=True, max_length=254)

    objects = SupplierUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username

class AdressUser(models.Model):
    cep = models.CharField(max_length=10)
    number = models.IntegerField()
    complement = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.cep

class BuyerUser(models.Model):
    user = models.OneToOneField(SupplierUser, on_delete=models.CASCADE, related_name='buyer_user', primary_key=True)
    cnpj = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=15)
    adress = models.OneToOneField(AdressUser, on_delete=models.CASCADE, related_name='buyer_adr')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.cnpj

