# Generated by Django 5.1.3 on 2024-11-29 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productlistApp', '0006_add_to_cart'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='add_to_cart',
            new_name='add_to_cart_list',
        ),
    ]
