from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(unique=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    def get_full_name(self):
        return f"{self.phone_number}"


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Mamlakat"))

    def __str__(self):
        return self.name

class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_("Mamlakat"))
    name = models.CharField(max_length=100, verbose_name=_("Viloyat"))

    def __str__(self):
        return self.name

class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name=_("Viloyat"))
    name = models.CharField(max_length=100, verbose_name=_("Tuman"))

    def __str__(self):
        return self.name

class Passport(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='passport')

    first_name = models.CharField(max_length=100, verbose_name=_("Ism"))
    second_name = models.CharField(max_length=100, verbose_name=_("Otasining ismi"))
    third_name = models.CharField(max_length=100, verbose_name=_("Familiya"))

    birth_date = models.DateField(verbose_name=_("Tug'ilgan sana"))
    passport_number = models.CharField(max_length=9, verbose_name=_("Pasport raqami"))
    jshshir = models.CharField(max_length=14, unique=True, verbose_name=_("JSHSHIR"))

    image = models.ImageField(upload_to='abituriyent/images/', verbose_name=_("Abituriyent rasmi(3x4)"))
    gender = models.CharField(max_length=1, choices=[('E', 'Erkak'), ('A', 'Ayol')], verbose_name=_("Jins"))

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name=_("Mamlakat"))
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, verbose_name=_("Viloyat"))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, verbose_name=_("Tuman"))

    home_address = models.CharField(max_length=255, verbose_name=_("Uy manzili"))
    passport_file = models.FileField(upload_to='abituriyent/passports/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Passport")
        verbose_name_plural = _("Passportlar")

    def __str__(self):
        return f"{self.first_name} {self.second_name} {self.third_name}"

    def get_full_name(self):
        return f"{self.third_name} {self.first_name} {self.second_name}"

    def get_full_address(self):
        return f"{self.region} {self.district} {self.home_address}"
