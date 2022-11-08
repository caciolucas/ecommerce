# Generated by Django 4.1.1 on 2022-11-08 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="name",
            field=models.CharField(max_length=150, unique=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="group",
            name="permissions",
            field=models.ManyToManyField(
                blank=True, to="authentication.permission", verbose_name="Permissions"
            ),
        ),
    ]