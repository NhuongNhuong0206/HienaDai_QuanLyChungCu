# Generated by Django 5.0.4 on 2024-04-20 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QlChungCu', '0003_rename_admin_letter_letters_admin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acount',
            name='avatar_acount',
            field=models.ImageField(upload_to='QlChungCu/%Y/%m'),
        ),
    ]
