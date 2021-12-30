from datetime import date
from django.db.models import Sum, Count, Prefetch
from django.db.models.functions import Coalesce
from django.db.models.expressions import F
from .models import Person

def prefetch_related_list():
    females = Person.objects.filter(gender='female')
    males = Person.objects.filter(gender='male')
    return  ['children_dad',
            'children_mom',
            Prefetch('children_dad', queryset=females, to_attr='children_dad_female'),
            Prefetch('children_dad', queryset=males, to_attr='children_dad_male'),
            Prefetch('children_mom', queryset=females, to_attr='children_mom_female'),
            Prefetch('children_mom', queryset=males, to_attr='children_mom_male')]