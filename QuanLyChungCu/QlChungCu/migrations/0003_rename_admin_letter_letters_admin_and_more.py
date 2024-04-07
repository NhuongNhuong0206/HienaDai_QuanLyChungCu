# Generated by Django 5.0.4 on 2024-04-07 09:16

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QlChungCu', '0002_acount_admin_people_apartnum_people_birthday_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='letters',
            old_name='admin_letter',
            new_name='admin',
        ),
        migrations.RenameField(
            model_name='people',
            old_name='name_user',
            new_name='name_people',
        ),
        migrations.AlterField(
            model_name='goods',
            name='img_goods',
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
        migrations.AlterField(
            model_name='letters',
            name='img_letter',
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
    ]