# Generated by Django 3.1.5 on 2021-02-17 13:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0036_auto_20210217_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonreview',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]