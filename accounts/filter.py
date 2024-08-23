
# filters.py
import django_filters
from django_filters import CharFilter
from .models import Order
from django.db.models import Q

# class OrderFilter(django_filters.FilterSet):
#     class Meta:
#         model = Order
#         fields = ['status']


# class OrderFilter(django_filters.FilterSet):
#     search = CharFilter(method='general_search', label='Search')

#     class Meta:
#         model = Order
#         fields = []

#     def general_search(self, queryset, name, value):
#         return queryset.filter(
#             Q(status__icontains=value) |
#             Q(customer__name__icontains=value) |
#             Q(date__icontains=value)
#         )

def order_search(queryset, search_term):
    return queryset.filter(
        Q(first_name__icontains=search_term) |
        Q(last_name__icontains=search_term) |
        Q(email__icontains=search_term) |
        Q(phone__icontains=search_term) |
        Q(destination__icontains=search_term) |
        Q(status__icontains=search_term) 
        
    )