# Generated by Django 3.1.5 on 2021-01-06 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='instructor_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lessons', to='profiles.userprofile'),
        ),
        migrations.AlterField(
            model_name='lessonitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.userprofile'),
        ),
    ]