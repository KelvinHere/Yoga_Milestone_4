# Generated by Django 3.1.5 on 2021-01-06 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_auto_20210106_0938'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='lesson_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='lesson_url',
            new_name='url',
        ),
    ]
