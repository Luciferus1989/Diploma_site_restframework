# Generated by Django 5.0.1 on 2024-01-10 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0010_rename_customer_name_feedback_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='author',
            field=models.CharField(max_length=50),
        ),
    ]