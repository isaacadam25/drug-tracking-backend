# Generated by Django 3.2 on 2021-07-14 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Makole', '0006_alter_makolebatch_unit_of_measure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makolebatch',
            name='unit_of_measure',
            field=models.CharField(blank=True, default='tablet', max_length=10),
        ),
    ]
