# Generated by Django 3.1.7 on 2024-06-05 02:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0009_auto_20240423_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paqueteturistico',
            name='disponibles',
        ),
    ]
