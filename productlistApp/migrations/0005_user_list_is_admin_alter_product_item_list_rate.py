# Generated by Django 5.1.3 on 2024-11-22 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productlistApp', '0004_product_item_list_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_list',
            name='is_admin',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product_item_list',
            name='Rate',
            field=models.CharField(default='0', max_length=255),
        ),
    ]
