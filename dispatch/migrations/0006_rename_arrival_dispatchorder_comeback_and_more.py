# Generated by Django 4.0.1 on 2022-03-21 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0005_alter_dispatchorder_total_distance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dispatchorder',
            old_name='arrival',
            new_name='comeback',
        ),
        migrations.RenameField(
            model_name='dispatchorder',
            old_name='arrival_date',
            new_name='comeback_date',
        ),
        migrations.RenameField(
            model_name='dispatchorder',
            old_name='arrival_time',
            new_name='comeback_time',
        ),
        migrations.AddField(
            model_name='dispatchorder',
            name='comeback_short',
            field=models.CharField(default='comeback_short', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dispatchorder',
            name='departure_short',
            field=models.CharField(default='daparture_short', max_length=64),
            preserve_default=False,
        ),
    ]