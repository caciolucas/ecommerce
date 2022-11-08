from rest_framework import viewsets, views
from rest_framework.decorators import action
from rest_framework.response import Response

from commerce.models import Product, Cart, Order
from commerce.serializers import ProductSerializer, CartSerializer, OrderSerializer


# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=False, methods=["post"], url_path="my-cart/add")
    def add_product(self, request):
        cart = Cart.objects.get(user=request.user)
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "Product ID is required."}, status=400)
        quantity = request.data.get("quantity", 1)
        cart.set_item(product_id, quantity)
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["delete"], url_path="my-cart/remove")
    def remove_product(self, request):
        cart = Cart.objects.get(user=request.user)
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "Product ID is required."}, status=400)
        cart.remove_item(product_id)
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["get"], url_path="my-cart")
    def my_cart(self, request):
        cart = Cart.objects.get(user=request.user)
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["post"], url_path="my-cart/finish")
    def finish_my_cart(self, request):
        cart = Cart.objects.get(user=request.user)
        cart.generate_order()
        return Response(status=201)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
