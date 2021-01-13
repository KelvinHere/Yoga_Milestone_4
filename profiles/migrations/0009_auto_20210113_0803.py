# Generated by Django 3.1.5 on 2021-01-13 08:03

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20210107_1947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='image_url',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, null=True, quality=0, size=[400, 600], upload_to='profile_images/'),
        ),
    ]