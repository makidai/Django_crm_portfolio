from django_filters import FilterSet, DateFilter, CharFilter

from .models import *

#カスタマーページでフィルター検索を実装
class OrderFilter(FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr='gte')
    end_date = DateFilter(field_name="date_created", lookup_expr='lte')
    note = CharFilter(field_name='note', lookup_expr='icontains')
    class Meta:
        model = Order
        fields = '__all__'
        exclude= ['customer','date_created']