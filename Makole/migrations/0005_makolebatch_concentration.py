# Generated by Django 3.2 on 2021-07-14 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Makole', '0004_makolebatch_quantity_received'),
    ]

    operations = [
        migrations.AddField(
            model_name='makolebatch',
            name='concentration',
            field=models.CharField(default='200mg', max_length=15),
            preserve_default=False,
        ),
    ]