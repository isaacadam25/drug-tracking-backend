# Generated by Django 3.2 on 2021-07-05 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DTS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='corresponding_transaction',
            field=models.CharField(blank=True, editable=False, max_length=20, null=True),
        ),
    ]
