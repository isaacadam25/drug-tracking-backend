# Generated by Django 3.2 on 2021-07-14 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0004_auto_20210714_0340'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitalbatch',
            name='concentration',
            field=models.CharField(default='200mg', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospitalbatch',
            name='quantity_received',
            field=models.IntegerField(default=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hospitalbatch',
            name='unit_of_measure',
            field=models.CharField(blank=True, choices=[('ml', 'ML'), ('cp', 'CP'), ('tb', 'TB')], default='tb', max_length=10),
        ),
    ]
