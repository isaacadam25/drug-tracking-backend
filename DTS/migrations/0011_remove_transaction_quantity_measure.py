# Generated by Django 3.2 on 2021-06-23 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DTS', '0010_batch_quantity_received'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='quantity_measure',
        ),
    ]
