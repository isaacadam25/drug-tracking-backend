# Generated by Django 3.2 on 2021-07-14 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DTS', '0005_alter_transaction_initiator'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpiredTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destruction_date', models.DateField()),
                ('quantity_destroyed', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DTS.institute')),
            ],
        ),
    ]