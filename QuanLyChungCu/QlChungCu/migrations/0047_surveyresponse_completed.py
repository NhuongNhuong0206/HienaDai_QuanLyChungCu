# Generated by Django 5.0.4 on 2024-06-11 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QlChungCu', '0046_rename_response_surveyresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresponse',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
