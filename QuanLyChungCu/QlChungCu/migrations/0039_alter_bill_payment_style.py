# Generated by Django 5.0.4 on 2024-05-26 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QlChungCu', '0038_bill_payment_style'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='payment_style',
            field=models.CharField(default='Null', max_length=255, null=True),
        ),
    ]
