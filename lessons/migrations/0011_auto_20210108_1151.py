# Generated by Django 3.1.5 on 2021-01-08 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0010_auto_20210108_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='lesson_images/'),
        ),
    ]
