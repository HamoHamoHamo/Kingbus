# Generated by Django 4.0.1 on 2022-03-03 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0003_rename_photo_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='photo',
            new_name='image',
        ),
        migrations.AlterModelTable(
            name='image',
            table='kingbus_community_image',
        ),
    ]
