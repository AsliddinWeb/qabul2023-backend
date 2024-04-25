from rest_framework import generics, permissions
from .models import Filial, TalimTuri, TalimShakli, Yonalish
from .serializers import FilialSerializer, TalimTuriSerializer, TalimShakliSerializer, YonalishSerializer
from .filters import YonalishFilter

class FilialListView(generics.ListAPIView):
    queryset = Filial.objects.all()
    serializer_class = FilialSerializer
    # permission_classes = [permissions.IsAuthenticated]

class TalimTuriListView(generics.ListAPIView):
    queryset = TalimTuri.objects.all()
    serializer_class = TalimTuriSerializer
    # permission_classes = [permissions.IsAuthenticated]

class TalimShakliListView(generics.ListAPIView):
    queryset = TalimShakli.objects.all()
    serializer_class = TalimShakliSerializer
    # permission_classes = [permissions.IsAuthenticated]

class YonalishListView(generics.ListAPIView):
    queryset = Yonalish.objects.all()
    serializer_class = YonalishSerializer
    filter_class = YonalishFilter
    # permission_classes = [permissions.IsAuthenticated]
