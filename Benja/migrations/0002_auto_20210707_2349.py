# Generated by Django 3.2 on 2021-07-07 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Benja', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patienttype',
            name='height',
            field=models.FloatField(default=1.5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patienttype',
            name='weight',
            field=models.FloatField(default=72.0),
            preserve_default=False,
        ),
    ]