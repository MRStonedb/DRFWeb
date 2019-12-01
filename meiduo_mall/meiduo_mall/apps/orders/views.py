from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated  # 权限验证，是否登录
from rest_framework.response import Response

from goods.models import SKU
from decimal import Decimal

from .serialziers import CartSKUSerializer, OrderSettlementSerializer, SaveOrderSerializer
# Create your views here.


class OrderSettlementView(APIView):
    """
    订单结算
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        获取
        """
        user = request.user

        # 从购物车中获取用户勾选要结算的商品信息
        redis_conn = get_redis_connection('cart')
        # redis中购物车商品信息  哈希
        redis_cart = redis_conn.hgetall('cart_%s' % user.id) # 
        # redis 中勾选状态， set类型
        cart_selected = redis_conn.smembers('cart_selected_%s' % user.id)

        cart = {}
        for sku_id in cart_selected:
            cart[int(sku_id)] = int(redis_cart[sku_id])

        # 查询商品信息
        skus = SKU.objects.filter(id__in=cart.keys())
        for sku in skus:
            sku.count = cart[sku.id]

        # 运费
        freight = Decimal('10.00')

        serializer = OrderSettlementSerializer({'freight': freight, 'skus': skus})
        return Response(serializer.data)


class SaveOrderView(CreateAPIView):
    """
    保存订单
    """
    serializer_class = SaveOrderSerializer
    permission_classes = [IsAuthenticated]

    # def post(self):
    #     # 接受参数  address pay_method
    #     # 校验
    #
    #     # 获取购物车勾选结算的数据
    #     # 创建订单保存
    #
    #     # 序列化返回
