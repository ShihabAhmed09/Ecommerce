import django_filters
from django import forms
from .models import *
from django.db.models import Q


class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_filter', label='Search products',
                                  widget=forms.TextInput(attrs={'placeholder': 'Search'}))

    class Meta:
        model = Product
        fields = ['q']

    def custom_filter(self, queryset, name, value):
        return Product.objects.filter(Q(name__icontains=value) | Q(tags__name__icontains=value)).distinct()
