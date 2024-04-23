from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import DiplomMalumotTuri, DiplomMuassasaTuri, Kurslar, Diplom, PerevodDiplom

@admin.register(DiplomMalumotTuri)
class DiplomMalumotTuriAdmin(admin.ModelAdmin):
    list_display = ['nomi']
    search_fields = ['nomi']

@admin.register(DiplomMuassasaTuri)
class DiplomMuassasaTuriAdmin(admin.ModelAdmin):
    list_display = ['nomi']
    search_fields = ['nomi']

@admin.register(Kurslar)
class KurslarAdmin(admin.ModelAdmin):
    list_display = ['kurs_nomi']
    search_fields = ['kurs_nomi']

@admin.register(Diplom)
class DiplomAdmin(admin.ModelAdmin):
    list_display = ['user', 'diplom_seriya', 'muassasa_nomi', 'tugatgan_yili']
    list_filter = ['muassasa_turi', 'malumot_turi', 'tugatgan_viloyati', 'tugatgan_tumani']
    search_fields = ['diplom_seriya', 'user__username', 'muassasa_nomi']
    autocomplete_fields = ['user', 'malumot_turi', 'muassasa_turi', 'tugatgan_viloyati', 'tugatgan_tumani']

@admin.register(PerevodDiplom)
class PerevodDiplomAdmin(admin.ModelAdmin):
    list_display = ['user', 'universitet_nomi', 'topshiradigan_kursi']
    list_filter = ['davlat', 'topshiradigan_kursi']
    search_fields = ['user__username', 'universitet_nomi']
    autocomplete_fields = ['user', 'davlat', 'topshiradigan_kursi']

