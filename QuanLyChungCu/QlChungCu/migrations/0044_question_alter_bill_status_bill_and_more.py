# Generated by Django 5.0.4 on 2024-06-11 10:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QlChungCu', '0043_goods_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='bill',
            name='status_bill',
            field=models.CharField(choices=[('Unpaid', 'Unpaid'), ('paid', 'Paid')], default='Unpaid', max_length=50),
        ),
        migrations.AlterField(
            model_name='goods',
            name='received_Goods',
            field=models.CharField(choices=[('Chờ nhận hàng', 'Wtr'), ('Đã lấy hàng', 'Received'), ('Người dùng đã nhận được hàng', 'Urg')], default='Chờ nhận hàng', max_length=50),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('respondent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QlChungCu.question')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='QlChungCu.response')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='KHAO SAT CHUNG CU HIEN VY', max_length=200)),
                ('note', models.CharField(max_length=200, null=True)),
                ('user_surveyor', models.ForeignKey(limit_choices_to={'user_role': 'Admin'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='response',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QlChungCu.survey'),
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='QlChungCu.survey'),
        ),
    ]
