from django.db import models

from django.utils.translation import gettext_lazy as _
from django.conf import settings

from auth_app.models import Country, Region, District

class DiplomMalumotTuri(models.Model):
    nomi = models.CharField(max_length=100, verbose_name=_("Ma'lumot turi"))

    def __str__(self):
        return self.nomi

class DiplomMuassasaTuri(models.Model):
    nomi = models.CharField(max_length=100, verbose_name=_("Muassasa turi"))

    def __str__(self):
        return self.nomi

class Kurslar(models.Model):
    kurs_nomi = models.CharField(max_length=255)

    def __str__(self):
        return self.kurs_nomi

class Diplom(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diplom')

    diplom_seriya = models.CharField(max_length=255)

    malumot_turi = models.ForeignKey(DiplomMalumotTuri, on_delete=models.CASCADE, verbose_name=_("Ma'lumot turi"))
    muassasa_turi = models.ForeignKey(DiplomMuassasaTuri, on_delete=models.CASCADE, verbose_name=_("Muassasa turi"))

    muassasa_nomi = models.TextField()
    tugatgan_yili = models.CharField(max_length=255)

    tugatgan_viloyati = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name=_("Viloyati"))
    tugatgan_tumani = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name=_("Tuman/Shahari"))

    diplom_fayl = models.FileField(upload_to='diplomlar/')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.diplom_seriya}"

class PerevodDiplom(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perevod_diplom')

    davlat = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_("Davlat"))

    universitet_nomi = models.TextField()
    transkript = models.FileField(upload_to='trasnkriptlar/')

    topshiradigan_kursi = models.ForeignKey(Kurslar, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()
