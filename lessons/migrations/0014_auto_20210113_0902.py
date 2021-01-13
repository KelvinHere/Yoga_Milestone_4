# Generated by Django 3.1.5 on 2021-01-13 09:02

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0013_auto_20210112_0934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='image_url',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='url',
        ),
        migrations.AlterField(
            model_name='lesson',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, null=True, quality=75, size=[600, 600], upload_to='lesson_images/'),
        ),
    ]
