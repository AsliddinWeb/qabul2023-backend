from django.urls import path
from .views import FilialListView, TalimTuriListView, TalimShakliListView, YonalishListView, RegisterSlayderListView

urlpatterns = [
    path('filiallar/', FilialListView.as_view(), name='filial-list'),
    path('talim-turlari/', TalimTuriListView.as_view(), name='talim-turi-list'),
    path('talim-shakllari/', TalimShakliListView.as_view(), name='talim-shakli-list'),
    path('yonalishlar/', YonalishListView.as_view(), name='yonalish-list'),
    path('register-motivation/', YonalishListView.as_view(), name='register-motivation-list'),
]
