# Generated by Django 3.2 on 2021-06-29 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DTS', '0001_initial'),
        ('MSD', '0003_auto_20210629_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DTS.institute'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(blank=True, default='incomplete', max_length=3),
        ),
    ]
