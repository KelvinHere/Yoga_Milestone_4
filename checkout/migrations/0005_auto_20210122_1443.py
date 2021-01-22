# Generated by Django 3.1.5 on 2021-01-22 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_order_stripe_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='original_basket',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='order',
            name='stripe_id',
            field=models.CharField(default='', max_length=254),
        ),
    ]
