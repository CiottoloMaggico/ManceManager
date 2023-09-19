import django_filters
from django.forms.widgets import DateInput, TextInput, Select
from .models import Activity, Category

class ActivityFilter(django_filters.FilterSet):
    date__lte = django_filters.DateFilter(
        lookup_expr='lte',
        field_name='date',
        widget=DateInput(
            attrs={
                'type':'date',
                'class':'form-control'
            }
        )
    )
    date__gte = django_filters.DateFilter(
        lookup_expr='gte',
        field_name='date',
        widget=DateInput(
            attrs={
                'type':'date', 'class':'form-control'
            }
        )
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        widget=Select(
            attrs={
                'class':'form-select'
            }
        )
    )

    class Meta:
        model = Activity
        fields = []

class ClientFilter(django_filters.FilterSet):
    business_name = django_filters.CharFilter(
        lookup_expr='iexact',
        field_name='business_name',
        widget=TextInput(
            attrs={
                'type':'text',
                'placeholder':'Ragione Sociale',
                'class':'form-control',
            }
        )
    )

class CategoryFilter(django_filters.FilterSet):
    category_name = django_filters.CharFilter(
        lookup_expr='iexact',
        field_name='category_name',
        widget=TextInput(
            attrs={
                'type':'text',
                'placeholder':'Nome categoria',
                'class':'form-control',
            }
        )
    )