# Generated by Django 3.2 on 2021-07-12 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Benja', '0003_auto_20210708_0039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patienttype',
            name='height',
        ),
        migrations.RemoveField(
            model_name='patienttype',
            name='weight',
        ),
    ]