# Generated by Django 5.0.1 on 2024-01-19 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0024_alter_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_type',
            field=models.CharField(choices=[('standard', 'standard'), ('express', 'express')], default='standard', max_length=20),
        ),
    ]
