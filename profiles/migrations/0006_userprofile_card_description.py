# Generated by Django 3.1.5 on 2021-01-07 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20210107_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='card_description',
            field=models.TextField(default=1, max_length=512),
            preserve_default=False,
        ),
    ]
