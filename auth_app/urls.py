from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (RegisterView, PassportDetailView, PassportListCreateView,
                    VerifyPhoneNumberView, ResendVerificationCodeView, ChangePasswordView, GetMeAPIView,
                    ForgotPasswordView, ResetPasswordVerifyView
                    )

urlpatterns = [
    # Authentication
    path('register/', swagger_auto_schema(tags=['Auth'], method='post')(RegisterView.as_view()), name='register'),
    path('login/', swagger_auto_schema(tags=['Auth'], method='post')(TokenObtainPairView.as_view()),
         name='token_obtain_pair'),
    path('token-refresh/', swagger_auto_schema(tags=['Auth'], method='post')(TokenRefreshView.as_view()),
         name='token_refresh'),
    path('verify-phone/', VerifyPhoneNumberView.as_view(), name='verify-phone'),
    path('resend-sms/', ResendVerificationCodeView.as_view(), name='resend-sms'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('getMe/', GetMeAPIView.as_view(), name='get-me'),

    # Forgot password
    path('reset-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password-verify/', ResetPasswordVerifyView.as_view(), name='reset-password-verify'),

    # Passport
    path('passports/', swagger_auto_schema(tags=['Passport'],
                                           methods=['get', 'post'])(PassportListCreateView.as_view()),
         name='passport-list'),
    path('passports/<int:pk>/', swagger_auto_schema(tags=['Passport detail'],
                                                    methods=['get', 'put', 'patch', 'delete'])(
        PassportDetailView.as_view()), name='passport-detail'),
]
