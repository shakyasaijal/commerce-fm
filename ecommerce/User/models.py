from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, UserManager
from django.db import models
from django.conf import settings
from datetime import datetime, timedelta

import jwt


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class AbstractTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.created_at

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    is_verified = models.BooleanField(
        null=False, blank=False, default=False)  # False = not verified
    google_id = models.CharField(max_length=255, null=True, blank=True)
    facebook_id = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        full_name = None
        if self.first_name or self.last_name:
            full_name = self.first_name + " " + self.last_name
        elif self.username:
            full_name = self.username
        else:
            full_name = self.email
        return full_name

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-is_active']


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CityFromIpAddress(models.Model):
    city = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = "City From Ip Address"
        verbose_name_plural = "Cities From Ip Address"


class IpAddress(models.Model):
    ip = models.GenericIPAddressField(protocol="both", unpack_ipv4=False, null=False, blank=False, unique=True)
    city = models.ForeignKey(CityFromIpAddress, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.ip
    
    class Meta:
        verbose_name = "Ip Address"
        verbose_name_plural = "Ip Addresses"


if settings.HAS_ADDITIONAL_USER_DATA:
    class UserProfile(models.Model):
        user = models.OneToOneField(
            User, verbose_name="User", on_delete=models.CASCADE, related_name="user_profile")
        district = models.ForeignKey("CartSystem.Location", null=True, blank=True, on_delete=models.CASCADE)
        phone = models.CharField(max_length=255, null=False, blank=False)
        address = models.CharField(max_length=255, null=False, blank=False)
        interested_category = models.ManyToManyField("Products.Category", blank=True,  related_name="users_interests")
        ip = models.ManyToManyField(IpAddress, blank=True, related_name="user_ip")

        def __str__(self):
            return self.phone

        def associated_user(self):
            return self.user.get_full_name()

        class Meta:
            verbose_name = "User Profile"
            verbose_name_plural = "Users Profile"
