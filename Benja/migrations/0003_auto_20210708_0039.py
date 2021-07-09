# Generated by Django 3.2 on 2021-07-07 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Benja', '0002_auto_20210707_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='height',
            field=models.FloatField(default=1.75),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='weight',
            field=models.FloatField(default=66.0),
            preserve_default=False,
        ),
    ]
