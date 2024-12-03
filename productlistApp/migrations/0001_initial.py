# Generated by Django 5.1.3 on 2024-11-18 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(max_length=255)),
                ('Mobile', models.CharField(max_length=255)),
                ('Passworld1', models.CharField(max_length=255)),
                ('Passworld2', models.CharField(max_length=255)),
                ('Otp', models.CharField(max_length=255)),
                ('Verified', models.BooleanField()),
            ],
        ),
    ]
