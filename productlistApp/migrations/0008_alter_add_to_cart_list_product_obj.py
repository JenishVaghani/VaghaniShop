# Generated by Django 5.1.3 on 2024-11-29 10:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productlistApp', '0007_rename_add_to_cart_add_to_cart_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_to_cart_list',
            name='Product_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productlistApp.product_item_list'),
        ),
    ]
