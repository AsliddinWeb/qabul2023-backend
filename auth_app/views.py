from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Passport
from .serializers import (RegisterSerializer, UserDetailSerializer, PassportSerializer, ChangePasswordSerializer,
                          PhoneNumberVerificationSerializer, PhoneNumberSerializer, UserGetMelSerializer,
                          ForgotPasswordSerializer, ResetPasswordVerifySerializer
                          )

from django.contrib.auth import get_user_model

User = get_user_model()

# Send sms
from utils.sms import send_sms
from utils.eskiz_auth import eskiz_auth

from random import randint
from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from config_app.models import SmsText, EskizBearerToken, EskizEmailAndPassword


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Send sms
            verify_code = randint(1000, 9999)
            cache.set(user.phone_number, verify_code, timeout=300)

            sms_text = SmsText.objects.last()
            eskiz_bearer_token = EskizBearerToken.objects.last()
            eskiz_email_and_password = EskizEmailAndPassword.objects.last()

            if sms_text and eskiz_bearer_token:
                sms_data = send_sms(
                    phone_number=user.phone_number,
                    text=sms_text.text,
                    code=verify_code,
                    bearer_token=eskiz_bearer_token.token
                )

                if sms_data['status_code'] == 200:
                    user_data = UserDetailSerializer(user).data
                    return Response({"data": user_data, "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi"},
                                    status=status.HTTP_201_CREATED)
                else:
                    new_token = eskiz_auth(eskiz_email_and_password.email, eskiz_email_and_password.password)
                    EskizBearerToken.objects.create(token=new_token)

                    sms_data = send_sms(
                        phone_number=user.phone_number,
                        text=sms_text.text,
                        code=verify_code,
                        bearer_token=new_token
                    )
                    user_data = UserDetailSerializer(user).data
                    return Response({"data": user_data, "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi"},
                                    status=status.HTTP_201_CREATED)
            else:
                Response({"message": "Eskiz login parollari yo'q!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Change password!",
        request_body=ChangePasswordSerializer,
        tags=['Auth'],
    )

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response({"message": "Password successfully changed."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyPhoneNumberView(APIView):
    @swagger_auto_schema(
        operation_description="Verify a phone number and activate a user if the verification code matches.",
        request_body=PhoneNumberVerificationSerializer,
        tags=['Auth'],
        responses={
            200: openapi.Response(description="Phone number verified and user activated", examples={
                "application/json": {"message": "Telefon raqam tasdiqlandi va foydalanuvchi faollashtirildi."}
            }),
            404: openapi.Response(description="User not found", examples={
                "application/json": {"error": "Bunday telefon raqamli foydalanuvchi topilmadi."}
            }),
            400: "Invalid input"
        }
    )

    def post(self, request, *args, **kwargs):
        serializer = PhoneNumberVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = User.objects.filter(phone_number=phone_number).first()
            if user:
                user.is_active = True
                user.save()
                return Response({"message": "Telefon raqam tasdiqlandi va foydalanuvchi faollashtirildi."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Bunday telefon raqamli foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationCodeView(APIView):
    @swagger_auto_schema(
        operation_description="Resend sms code.",
        request_body=PhoneNumberSerializer,
        tags=['Auth'],
        responses={
            200: openapi.Response(description="Resend sms code", examples={
                "application/json": {"message": "Sms kod qaytadan yuborildi."}
            }),
            404: openapi.Response(description="Bunday foydalanuvchi yo'q", examples={
                "application/json": {"error": "Bunday telefon raqamli foydalanuvchi topilmadi."}
            }),
            400: "Invalid input"
        }
    )

    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            # Foydalanuvchini tekshiramiz
            if not User.objects.filter(phone_number=phone_number).exists():
                return Response({"error": "Bunday telefon raqamli foydalanuvchi topilmadi."},
                                status=status.HTTP_404_NOT_FOUND)

            if cache.get(phone_number):
                return Response({"error": "Kod yuborilgan!"},
                                status=status.HTTP_400_BAD_REQUEST)

            cache.delete(phone_number)

            # Yangi kodni yuboramiz
            verify_code = randint(1000, 9999)
            cache.set(phone_number, verify_code, timeout=300)

            sms_text = SmsText.objects.last()
            eskiz_bearer_token = EskizBearerToken.objects.last()
            eskiz_email_and_password = EskizEmailAndPassword.objects.last()

            if sms_text and eskiz_bearer_token:
                sms_data = send_sms(
                    phone_number=phone_number,
                    text=sms_text.text,
                    code=verify_code,
                    bearer_token=eskiz_bearer_token.token
                )

                if sms_data['status_code'] == 200:
                    return Response({"message": "Sms kod yuborildi."}, status=status.HTTP_200_OK)
                else:
                    new_token = eskiz_auth(eskiz_email_and_password.email, eskiz_email_and_password.password)
                    EskizBearerToken.objects.create(token=new_token)

                    sms_data = send_sms(
                        phone_number=phone_number,
                        text=sms_text.text,
                        code=verify_code,
                        bearer_token=new_token
                    )
                    return Response({"message": "Sms kod yuborildi."}, status=status.HTTP_200_OK)
            else:
                Response({"message": "Eskiz login parollari yo'q!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PassportListCreateView(ListCreateAPIView):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        user_id = request.data.get('user')
        user = get_object_or_404(User, pk=user_id)
        if not user.is_active:
            return Response({"detail": "Only active users can create passports."}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PassportDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer
    permission_classes = [
        permissions.IsAuthenticated]

    def get_object(self):
        obj = Passport.objects.get(pk=self.kwargs['pk'])

        if obj.user != self.request.user:
            raise PermissionDenied("Siz ushbu ma'lumotni ko'rishga ruxsatga ega emassiz")

        return obj

class GetMeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserGetMelSerializer(user)
        return Response(serializer.data)


class ForgotPasswordView(APIView):
    @swagger_auto_schema(
        operation_description="Forgot Password!",
        request_body=ForgotPasswordSerializer,
        tags=['Auth'],
    )

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verify_code = randint(1000, 9999)
            cache.set(phone_number, verify_code, timeout=300)  # Save the code in the cache for 5 minutes

            sms_text = SmsText.objects.last()
            eskiz_bearer_token = EskizBearerToken.objects.last()

            if sms_text and eskiz_bearer_token:
                send_sms(
                    phone_number=phone_number,
                    text=sms_text.text,
                    code=verify_code,
                    bearer_token=eskiz_bearer_token.token
                )
                return Response({"message": "Tasdiqlash kodi yuborildi."}, status=status.HTTP_200_OK)
            return Response({"error": "Sms yuborishda muammo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordVerifyView(APIView):
    @swagger_auto_schema(
        operation_description="Reset Password Verify!",
        request_body=ResetPasswordVerifySerializer,
        tags=['Auth'],
    )
    def post(self, request):
        serializer = ResetPasswordVerifySerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            User = get_user_model()
            user = User.objects.get(phone_number=phone_number)
            user.set_password('1234')  # Reset the password to '1234'
            user.save()
            cache.delete(phone_number)  # Clear the verification code from cache
            return Response({"message": "Parol muvaffaqiyatli yangilandi."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)