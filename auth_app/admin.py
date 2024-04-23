from django.contrib import admin
from .models import Country, Region, District, Passport
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name']
    list_filter = ['country']

class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'region']
    search_fields = ['name']
    list_filter = ['region']

class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = ('phone_number', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser', 'is_active', 'user_permissions', 'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups'),
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ('user_permissions', 'groups')

class PassportAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'second_name', 'third_name', 'passport_number', 'jshshir', 'birth_date', 'gender', 'country', 'region', 'district', 'home_address', 'created_at', 'updated_at']
    list_filter = ['gender', 'country', 'region', 'district', 'created_at']
    search_fields = ['first_name', 'second_name', 'third_name', 'passport_number', 'jshshir']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (_("Asosiy ma'lumotlar"), {'fields': ('user', 'first_name', 'second_name', 'third_name', 'birth_date', 'passport_number', 'jshshir')}),
        (_("Qo'shimcha ma'lumotlar"), {'fields': ('image', 'gender', 'country', 'region', 'district', 'home_address', 'passport_file')}),
        (_("Timestamps"), {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Passport, PassportAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
