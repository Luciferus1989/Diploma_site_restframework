# Generated by Django 5.0.1 on 2024-01-17 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0020_alter_order_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('pending', 'pending'), ('in process', 'in process'), ('archived', 'Archived')], default='active', max_length=10),
        ),
    ]
