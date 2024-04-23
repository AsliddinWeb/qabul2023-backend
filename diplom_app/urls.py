from django.urls import path
from .views import DiplomMalumotTuriListView, DiplomMuassasaTuriListView, KurslarListView, DiplomViewSet, PerevodDiplomViewSet

urlpatterns = [
    path('malumot-turlari/', DiplomMalumotTuriListView.as_view(), name='diplom-malumot-turi-list'),
    path('muassasa-turlari/', DiplomMuassasaTuriListView.as_view(), name='diplom-muassasa-turi-list'),
    path('mavjud-kurslar/', KurslarListView.as_view(), name='kurslar-list'),

    path('', DiplomViewSet.as_view(), name='diplom-list-create'),
    path('perevod-diplom/', PerevodDiplomViewSet.as_view(), name='perevod-diplom-list-create'),
]
