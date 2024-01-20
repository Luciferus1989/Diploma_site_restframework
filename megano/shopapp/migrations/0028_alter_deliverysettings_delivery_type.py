# Generated by Django 5.0.1 on 2024-01-19 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0027_alter_order_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverysettings',
            name='delivery_type',
            field=models.CharField(choices=[('ordinary', 'Обычная'), ('express', 'Экспресс-доставка')], max_length=20),
        ),
    ]