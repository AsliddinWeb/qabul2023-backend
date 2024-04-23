from django.contrib import admin
from .models import Filial, TalimTuri, TalimShakli, Yonalish

class FilialAdmin(admin.ModelAdmin):
    list_display = ('nomi',)
    search_fields = ('nomi',)

admin.site.register(Filial, FilialAdmin)

class TalimTuriAdmin(admin.ModelAdmin):
    list_display = ('nomi',)
    search_fields = ('nomi',)

admin.site.register(TalimTuri, TalimTuriAdmin)

class TalimShakliAdmin(admin.ModelAdmin):
    list_display = ('nomi',)
    search_fields = ('nomi',)

admin.site.register(TalimShakli, TalimShakliAdmin)

class YonalishAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'filial', 'talim_turi', 'talim_shakli', 'kontrakt_narxi', 'shartnoma_seriyasi')
    list_filter = ('filial', 'talim_turi', 'talim_shakli')
    search_fields = ('nomi', 'kontrakt_narxi', 'shartnoma_seriyasi')
    # raw_id_fields = ('filial', 'talim_turi', 'talim_shakli')

admin.site.register(Yonalish, YonalishAdmin)
