# Generated by Django 5.0.1 on 2024-01-12 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0013_alter_item_description'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderItem',
            new_name='Basket',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='customer_name',
            new_name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='promocode',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.CharField(default='on-line', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('accepted', 'accepted'), ('payed', 'payed'), ('archived', 'Archived')], default='active', max_length=10),
        ),
    ]
