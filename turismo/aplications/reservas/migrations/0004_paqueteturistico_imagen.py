# Generated by Django 3.1.7 on 2024-04-21 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0003_auto_20240420_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='paqueteturistico',
            name='imagen',
            field=models.ImageField(null=True, upload_to='static/imagenes/'),
        ),
    ]
