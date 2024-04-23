from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import DiplomMalumotTuri, DiplomMuassasaTuri, Kurslar, Diplom, PerevodDiplom
from .serializers import (DiplomMalumotTuriSerializer, DiplomMuassasaTuriSerializer,
                          KurslarSerializer, DiplomSerializer, PerevodDiplomSerializer)


from django.contrib.auth import get_user_model

User = get_user_model()

class DiplomMalumotTuriListView(generics.ListAPIView):
    queryset = DiplomMalumotTuri.objects.all()
    serializer_class = DiplomMalumotTuriSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List Diploma Education Types",
        operation_description="Retrieves a list of all diploma education types.",
        tags=['Diplom']
    )
    def get(self, request, *args, **kwargs):
        """ Lists all diploma education types. """
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class DiplomMuassasaTuriListView(generics.ListAPIView):
    queryset = DiplomMuassasaTuri.objects.all()
    serializer_class = DiplomMuassasaTuriSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List Diploma Institution Types",
        operation_description="Retrieves a list of all diploma institution types.",
        tags=['Diplom']
    )
    def get(self, request, *args, **kwargs):
        """ Lists all diploma institution types. """
        return super().get(request, *args, **kwargs)

class KurslarListView(generics.ListAPIView):
    queryset = Kurslar.objects.all()
    serializer_class = KurslarSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List Courses",
        operation_description="Retrieves a list of all courses available.",
        tags=['Diplom']
    )
    def get(self, request, *args, **kwargs):
        """ Lists all courses. """
        return super().get(request, *args, **kwargs)

class DiplomViewSet(generics.ListCreateAPIView):
    queryset = Diplom.objects.all()
    serializer_class = DiplomSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List and Create Diplomas",
        operation_description="Retrieves a list of diplomas or creates a new diploma.",
        tags=['Diplom']
    )
    def get(self, request, *args, **kwargs):
        """ Lists all diplomas. """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Diploma",
        operation_description="Creates a new diploma.",
        tags=['Diplom']
    )

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        user = get_object_or_404(User, pk=user_id)
        if not user.is_active:
            return Response({"detail": "Only active users can create passports."}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)

class PerevodDiplomViewSet(generics.ListCreateAPIView):
    queryset = PerevodDiplom.objects.all()
    serializer_class = PerevodDiplomSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List and Create Diploma Transfers",
        operation_description="Retrieves a list of diploma transfers or creates a new diploma transfer.",
        tags=['Diplom']
    )
    def get(self, request, *args, **kwargs):
        """ Lists all diploma transfers. """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Diploma Transfer",
        operation_description="Creates a new diploma transfer.",
        tags=['Diplom']
    )
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        user = get_object_or_404(User, pk=user_id)
        if not user.is_active:
            return Response({"detail": "Only active users can create passports."}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)
