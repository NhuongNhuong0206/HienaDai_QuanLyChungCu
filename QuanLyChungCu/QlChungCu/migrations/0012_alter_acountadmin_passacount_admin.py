# Generated by Django 5.0.4 on 2024-05-01 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QlChungCu', '0011_alter_acountadmin_passacount_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acountadmin',
            name='passacount_admin',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
