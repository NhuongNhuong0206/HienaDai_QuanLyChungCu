# Generated by Django 5.0.4 on 2024-05-09 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QlChungCu', '0020_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='carcard',
            name='status_car',
            field=models.CharField(choices=[('Unconfimred', 'Un'), ('Wait_for_confirmation', 'Wait'), ('Confirmed', 'Confirmer')], default='Unconfimred', max_length=50),
        ),
        migrations.AddField(
            model_name='carcard',
            name='vehicle_type',
            field=models.CharField(default='motorbike', max_length=255),
        ),
    ]
