# Generated by Django 3.1.5 on 2021-01-21 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_auto_20210121_1647'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='user',
            new_name='profile',
        ),
        migrations.RenameField(
            model_name='orderlineitem',
            old_name='user',
            new_name='profile',
        ),
    ]
