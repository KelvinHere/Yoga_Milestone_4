# Generated by Django 3.1.5 on 2021-01-13 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_auto_20210113_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='requested_instructor_status',
            field=models.BooleanField(default=False),
        ),
    ]
