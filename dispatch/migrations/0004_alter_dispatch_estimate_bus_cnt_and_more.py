# Generated by Django 4.0.1 on 2022-02-16 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0003_alter_dispatch_estimate_driverorcompany'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispatch_estimate',
            name='bus_cnt',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='dispatch_estimate',
            name='bus_type',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='dispatch_estimate',
            name='price',
            field=models.CharField(max_length=10),
        ),
    ]
