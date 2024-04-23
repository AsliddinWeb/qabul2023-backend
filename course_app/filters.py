from django_filters import rest_framework as filters
from .models import Yonalish

class YonalishFilter(filters.FilterSet):
    class Meta:
        model = Yonalish
        fields = {
            'filial': ['exact'],
            'talim_turi': ['exact'],
            'talim_shakli': ['exact'],
        }
