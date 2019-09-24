from django.shortcuts import render
# Create your views here.


from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from .serializers import SKUSerializer
from .models import SKU

# /categories/(?P<category_id>\d+)/skus?page=xxx&page_size=xxx&ordering=xxx
class SKUListView(ListAPIView):
    """
    sku列表数据
    """
    serializer_class = SKUSerializer
    filter_backends = (OrderingFilter,)
    # 排序规则， 时间，价格，销量
    ordering_fields = ('create_time', 'price', 'sales')

    #分页为全局设置

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        # 筛选条件 ：category_id（在SKU模型中作为外键，所以有category_id字段），is_launched 是新上架
        return SKU.objects.filter(category_id=category_id, is_launched=True)