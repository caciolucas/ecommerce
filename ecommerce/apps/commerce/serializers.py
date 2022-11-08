from rest_framework import serializers

from authentication.models import User
from commerce.models import Product, ProductImage, Cart, CartItem, Order


class ProductImageSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        fields = "__all__"
        model = ProductImage


class ProductSerializer(serializers.ModelSerializer):
    images_display = ProductImageSerializer(many=True, read_only=True, source="images")

    class Meta:
        fields = "__all__"
        model = Product


class CartItemSerializer(serializers.ModelSerializer):
    product_display = ProductSerializer(read_only=True, source="product")
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        exclude = ("cart",)
        model = CartItem


class CartSerializer(serializers.ModelSerializer):
    items_display = serializers.SerializerMethodField()

    class Meta:
        fields = "__all__"
        model = Cart

    def get_items_display(self, obj):
        return CartItemSerializer(obj.items.all(), many=True).data

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        cart = Cart.objects.create(**validated_data)
        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)
        return cart


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Order
