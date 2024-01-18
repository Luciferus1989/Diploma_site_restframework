# Generated by Django 5.0.1 on 2024-01-17 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0021_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_type',
            field=models.CharField(choices=[('standard', 'standard'), ('express', 'express')], default='express', max_length=20),
            preserve_default=False,
        ),
    ]