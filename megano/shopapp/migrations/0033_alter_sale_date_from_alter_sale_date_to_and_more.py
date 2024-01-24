# Generated by Django 5.0.1 on 2024-01-24 22:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0032_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date_from',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='sale',
            name='date_to',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='sale',
            name='discount',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopapp.item')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopapp.sale')),
            ],
        ),
    ]
