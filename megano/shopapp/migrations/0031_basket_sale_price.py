# Generated by Django 5.0.1 on 2024-01-24 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0030_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='sale_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
