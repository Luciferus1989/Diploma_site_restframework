# Generated by Django 5.0.1 on 2024-01-15 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0016_alter_order_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('accepted', 'accepted'), ('in process', 'in process'), ('archived', 'Archived')], default='active', max_length=10),
        ),
    ]
