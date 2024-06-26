# Generated by Django 5.0.4 on 2024-05-26 06:43

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QlChungCu', '0036_people_identification_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='trading_code',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bill',
            name='transaction_images',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True),
        ),
    ]
