from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Shartnoma

@admin.register(Shartnoma)
class ShartnomaAdmin(admin.ModelAdmin):
    list_display = ('user', 'apply', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'apply__id')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user', 'apply')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'apply')
        }),
        (_('Shartnoma ma\'lumotlari'), {  # "Contract Information" section in Uzbek
            'fields': ('shartnoma_fayl',)
        }),
        (_('Vaqt belgilari'), {  # "Timestamps" in Uzbek
            'fields': (('created_at', 'updated_at'),)
        }),
    )
