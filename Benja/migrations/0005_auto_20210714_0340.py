# Generated by Django 3.2 on 2021-07-14 00:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Benja', '0004_auto_20210712_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='benjabatch',
            name='expiry_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='benjabatch',
            name='medicine_brand',
            field=models.CharField(max_length=50),
        ),
    ]
