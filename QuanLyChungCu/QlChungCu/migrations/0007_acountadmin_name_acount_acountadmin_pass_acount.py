# Generated by Django 5.0.4 on 2024-04-29 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QlChungCu', '0006_acountadmin_alter_acount_admin_alter_box_admin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='acountadmin',
            name='name_acount',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='acountadmin',
            name='pass_acount',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
