# Generated by Django 3.2 on 2021-08-08 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DTS', '0006_expiredtable'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='used',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]