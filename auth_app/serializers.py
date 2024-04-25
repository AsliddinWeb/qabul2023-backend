from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# Sms
from django.core.cache import cache

from .models import Passport, District, Region, Country

from diplom_app.serializers import DiplomSerializer, PerevodDiplomSerializer
from apply_app.serializers import ApplicationSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'password2')
        extra_kwargs = {'phone_number': {'required': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Parollar mos kelmaydi."})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'is_active']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)

    def validate_phone_number(self, value):
        if not value.startswith('+') or not value[1:].isdigit():
            raise serializers.ValidationError(
                "Notog'ri telefon raqami formati. Raqam '+' belgisi bilan boshlanishi kerak.")
        return value


class PhoneNumberVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    verify_code = serializers.CharField(max_length=6)

    def validate_phone_number(self, value):
        # Telefon raqamini tekshirish logikasi
        # Misol uchun, raqam formatini yoki ro'yxatdan o'tganligini tekshirish
        if not value.startswith('+') or not value[1:].isdigit():
            raise serializers.ValidationError(
                "Notog'ri telefon raqami formati. Raqam '+' belgisi bilan boshlanishi kerak.")
        return value

    def validate_verify_code(self, value):
        # Tasdiqlash kodini tekshirish
        # Ushbu kodni bazadan yoki cache'dan tekshirish mumkin
        if not value.isdigit():
            raise serializers.ValidationError("Tasdiqlash kodi faqat raqamlardan iborat bo'lishi kerak.")
        return value

    def validate(self, data):
        # Umumiy validatsiya
        phone_number = data.get('phone_number')
        verify_code = data.get('verify_code')

        if not self.check_verification_code(phone_number, verify_code):
            raise serializers.ValidationError("Tasdiqlash kodi noto'g'ri yoki muddati o'tgan.")

        return data

    def check_verification_code(self, phone_number, verify_code):
        # Cache'dan tasdiqlash kodini olish
        cached_code = cache.get(phone_number)

        return cached_code == int(verify_code)

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'country']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'region']

class PassportSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    country = CountrySerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)

    class Meta:
        model = Passport
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is not correct.")
        return value

    def validate_new_password(self, value):
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class UserGetMelSerializer(serializers.ModelSerializer):
    passport = PassportSerializer(read_only=True)
    diplom = DiplomSerializer(read_only=True)
    perevod_diplom = PerevodDiplomSerializer(read_only=True)
    application = ApplicationSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'is_active', 'passport', 'diplom', 'perevod_diplom', 'application']


class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)

    def validate_phone_number(self, value):
        User = get_user_model()
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Bunday telefon raqamli foydalanuvchi topilmadi.")
        return value

class ResetPasswordVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    verify_code = serializers.CharField(max_length=6)

    def validate(self, data):
        phone_number = data.get('phone_number')
        verify_code = data.get('verify_code')
        cached_code = cache.get(phone_number)

        if cached_code is None or str(cached_code) != verify_code:
            raise serializers.ValidationError("Tasdiqlash kodi noto'g'ri yoki muddati o'tgan.")
        return data