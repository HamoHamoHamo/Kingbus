# Generated by Django 4.0.1 on 2022-02-17 01:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=16)),
                ('num', models.CharField(max_length=12, unique=True)),
                ('role', models.CharField(max_length=1)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'kingbus_user',
            },
        ),
        migrations.CreateModel(
            name='DriverAcc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_com_name', models.CharField(max_length=32)),
                ('driver_car_driverlicense', models.ImageField(upload_to=user.models.upload_to_func_driver_car_driverlicense)),
                ('driver_car_option', models.CharField(blank=True, max_length=128, null=True)),
                ('driver_car_num', models.CharField(blank=True, max_length=10, null=True)),
                ('driver_car_kind', models.CharField(blank=True, max_length=32, null=True)),
                ('driver_car_year', models.CharField(blank=True, max_length=4, null=True)),
                ('driver_car_photo', models.ImageField(blank=True, null=True, upload_to=user.models.upload_to_func_driver_car_photo)),
                ('driver_profile_tradeunion_certificate', models.FileField(blank=True, null=True, upload_to=user.models.upload_to_func_driver_profile_tradeunion_certificate)),
                ('driver_profile_introduction', models.CharField(blank=True, max_length=200, null=True)),
                ('driver_profile_introduction_video', models.TextField(blank=True, null=True)),
                ('driver_profile_location', models.CharField(blank=True, max_length=128, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kingbus_driver_profile',
            },
        ),
        migrations.CreateModel(
            name='CompanyAcc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_com_name', models.CharField(max_length=32)),
                ('company_business_registration', models.ImageField(upload_to=user.models.upload_to_func_company_business_registration)),
                ('company_profile_transportationbusiness_registration', models.ImageField(blank=True, null=True, upload_to=user.models.upload_to_func_company_profile_transportationbusiness_registration)),
                ('company_profile_tradeunion_certificate', models.FileField(blank=True, null=True, upload_to=user.models.upload_to_func_company_profile_tradeunion_certificate)),
                ('company_profile_introduction', models.CharField(blank=True, max_length=200, null=True)),
                ('company_profile_introduction_video', models.TextField(blank=True, null=True)),
                ('company_profile_location', models.CharField(blank=True, max_length=128, null=True)),
                ('company_profile_companylocation', models.CharField(blank=True, max_length=128, null=True)),
                ('company_profile_vehiclecount', models.CharField(blank=True, max_length=8, null=True)),
                ('company_code', models.CharField(blank=True, max_length=12, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kingbus_company_profile',
            },
        ),
    ]
