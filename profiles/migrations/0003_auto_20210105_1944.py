# Generated by Django 3.1.5 on 2021-01-05 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20210105_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructorprofile',
            name='is_instructor',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='is_instructor',
            field=models.BooleanField(default=False),
        ),
    ]
