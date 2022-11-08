from django.db import models
from common.models import AutoTimestampedModel, UUIDModel
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Product(AutoTimestampedModel, UUIDModel):
    name = models.CharField("Nome", max_length=255)
    description = models.TextField("Descrição")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name


class ProductImage(AutoTimestampedModel, UUIDModel):
    product = models.ForeignKey("commerce.Product", related_name="images", on_delete=models.CASCADE)
    product_image = models.FileField("Imagem")
    description = models.TextField("Descrição")

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return f'{self.product.name} - {self.description}'


class Order(AutoTimestampedModel, UUIDModel):
    user = models.ForeignKey("authentication.User", related_name="orders", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(AutoTimestampedModel, UUIDModel):
    order = models.ForeignKey("commerce.Order", related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("commerce.Product", related_name="order_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Quantidade")

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")


class Cart(AutoTimestampedModel, UUIDModel):
    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return f'{self.user.username} - {self.created_at} {len(self.items.all())} items'

    def generate_order(self):
        order = Order.objects.create(user=self.user)
        for item in self.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        self.items.all().delete()
        return order

    def set_item(self, product_id, quantity):
        cart_item = self.items.filter(product_id=product_id).first()
        if cart_item:
            if quantity == 0:
                cart_item.delete()
            cart_item.quantity = quantity
            cart_item.save()
        else:
            CartItem.objects.create(cart=self, product_id=product_id, quantity=quantity)


class CartItem(AutoTimestampedModel, UUIDModel):
    cart = models.ForeignKey("commerce.Cart", related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("commerce.Product", related_name="cart_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Quantidade")

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")

    def __str__(self):
        return f'{self.product.name} - {self.quantity} ({self.cart.user.username})'
