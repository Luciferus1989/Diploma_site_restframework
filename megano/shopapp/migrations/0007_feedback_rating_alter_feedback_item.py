# Generated by Django 5.0.1 on 2024-01-05 02:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0006_rename_image_itemimage_src'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='rating',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='shopapp.item'),
        ),
    ]
