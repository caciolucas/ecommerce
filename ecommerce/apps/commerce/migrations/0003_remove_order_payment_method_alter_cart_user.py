# Generated by Django 4.1.1 on 2022-11-08 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("commerce", "0002_cart_cartitem_order_orderitem_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="payment_method",
        ),
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
