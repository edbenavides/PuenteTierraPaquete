# Generated by Django 3.1.7 on 2024-08-21 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0055_auto_20240820_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='password',
        ),
    ]
