# Generated by Django 5.0.1 on 2024-01-24 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0034_sale_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]