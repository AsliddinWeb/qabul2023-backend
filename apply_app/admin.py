from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ApplyStatus, Application

@admin.register(ApplyStatus)
class ApplyStatusAdmin(admin.ModelAdmin):
    list_display = ('nomi',)
    search_fields = ('nomi',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'filial', 'talim_turi', 'talim_shakli', 'yonalish', 'apply_status', 'created_at', 'updated_at')
    list_filter = ('apply_status', 'filial', 'talim_turi', 'talim_shakli', 'yonalish')
    search_fields = ('user__username', 'filial__nomi', 'talim_turi__nomi', 'talim_shakli__nomi', 'yonalish__nomi')
    # raw_id_fields = ('user', 'passport', 'diplom', 'perevod_diplom')
    # autocomplete_fields = ['passport', 'diplom', 'perevod_diplom']
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_("User Information"), {'fields': ('user', 'passport')}),
        (_("Education Details"), {'fields': ('diplom', 'perevod_diplom', 'is_perevod')}),
        (_("Program Information"), {'fields': ('filial', 'talim_turi', 'talim_shakli', 'yonalish')}),
        (_("Application Status"), {'fields': ('apply_status',)}),
        (_("Dates"), {'fields': ('created_at', 'updated_at')}),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
