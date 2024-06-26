# Generated by Django 5.0.4 on 2024-05-08 04:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QlChungCu', '0013_acount_update_acount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='people',
            name='acount',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='Acount_id',
        ),
        migrations.RemoveField(
            model_name='car_card',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='letters',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='box',
            name='admin',
        ),
        migrations.AddField(
            model_name='bill',
            name='user_resident',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='box',
            name='user_admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='letters',
            name='user_admin',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='people',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_acount',
            field=models.ImageField(null=True, upload_to='QlChungCu/%Y/%m'),
        ),
        migrations.AddField(
            model_name='user',
            name='change_password_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, verbose_name='username'),
        ),
        migrations.CreateModel(
            name='CarCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('area', models.CharField(max_length=255)),
                ('user_admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='people',
            name='car_card',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='QlChungCu.carcard'),
        ),
        migrations.DeleteModel(
            name='Acount',
        ),
        migrations.DeleteModel(
            name='AcountAdmin',
        ),
        migrations.DeleteModel(
            name='Car_card',
        ),
    ]
