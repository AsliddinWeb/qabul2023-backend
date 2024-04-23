from django.urls import path
from .views import ApplicationListCreateAPIView, ApplicationRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('applications/', ApplicationListCreateAPIView.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', ApplicationRetrieveUpdateDestroyAPIView.as_view(), name='application-detail'),
]
