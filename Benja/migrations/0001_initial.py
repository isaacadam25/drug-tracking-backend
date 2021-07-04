# Generated by Django 3.2 on 2021-07-04 11:42

import Benja.hospital_models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_number', models.CharField(blank=True, default=Benja.hospital_models.Appointment.generate_num, editable=False, max_length=10, unique=True)),
                ('status', models.CharField(blank=True, choices=[('pending', 'Pending'), ('active', 'Active'), ('complete', 'Complete')], default='pending', max_length=10)),
                ('date_of_appointment', models.DateField(auto_now_add=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BenjaBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_number', models.IntegerField(unique=True)),
                ('unit_of_measure', models.CharField(blank=True, choices=[('ml', 'ML'), ('cp', 'CP'), ('tb', 'TB')], default='tb', max_length=2)),
                ('quantity_measure', models.IntegerField()),
                ('medicine_name', models.CharField(max_length=30)),
                ('manufacturing_date', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BenjaMedicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serialnumber', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('t_quantity', models.IntegerField()),
                ('tq_used', models.IntegerField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=30)),
                ('price', models.FloatField()),
                ('description', models.TextField(blank=True, null=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Benja.benjabatch')),
            ],
        ),
        migrations.CreateModel(
            name='HospitalRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=5)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Labtest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_test', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Benja.appointment')),
            ],
        ),
        migrations.CreateModel(
            name='MedicineBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MSDZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone_name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.IntegerField()),
                ('total_quantity', models.IntegerField()),
                ('order_price', models.FloatField()),
                ('order_date', models.DateTimeField()),
                ('order_status', models.CharField(max_length=3)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PatientType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('contacts', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.IntegerField(unique=True)),
                ('date_issued', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('gender', models.BooleanField()),
                ('actual_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='benja_users', to=settings.AUTH_USER_MODEL)),
                ('room', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staffs_room', to='Benja.hospitalroom')),
                ('user_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Benja.usertype')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('is_sold', models.BooleanField(blank=True, default=False)),
                ('sid', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Benja.appointment')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Benja.benjabatch')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('other_name', models.CharField(blank=True, max_length=20, null=True)),
                ('is_male', models.BooleanField()),
                ('serial_number', models.CharField(blank=True, default=Benja.hospital_models.Patient.generate_num, editable=False, max_length=10, unique=True)),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=20)),
                ('contacts', models.CharField(blank=True, max_length=20, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('patient_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Benja.patienttype')),
            ],
        ),
        migrations.CreateModel(
            name='OrderedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Benja.benjamedicine')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Benja.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='order_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Benja.ordertype'),
        ),
        migrations.AddField(
            model_name='order',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Benja.supplier'),
        ),
        migrations.CreateModel(
            name='LabTestItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('results', models.TextField()),
                ('comments', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Benja.labtest')),
            ],
        ),
        migrations.AddField(
            model_name='labtest',
            name='technician',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Benja.userprofile'),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_on_invoice', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.FloatField()),
                ('status', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Benja.order')),
            ],
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnoses', models.TextField(null=True)),
                ('complaints', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Benja.appointment')),
            ],
        ),
        migrations.AddField(
            model_name='benjamedicine',
            name='msd_zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Benja.msdzone'),
        ),
        migrations.AddField(
            model_name='benjabatch',
            name='medicine_brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Benja.medicinebrand'),
        ),
        migrations.CreateModel(
            name='AppointmentFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('is_paid', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Benja.patient')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Benja.transaction')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Benja.userprofile'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Benja.patient'),
        ),
    ]
