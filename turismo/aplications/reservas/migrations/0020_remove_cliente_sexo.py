# Generated by Django 3.1.7 on 2024-06-18 03:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0019_cliente_sexo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='sexo',
        ),
    ]
