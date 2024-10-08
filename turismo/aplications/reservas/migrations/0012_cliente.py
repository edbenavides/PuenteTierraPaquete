# Generated by Django 3.1.7 on 2024-06-05 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0011_auto_20240604_2156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=11, unique=True)),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.CharField(max_length=15)),
                ('paquete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservas.paqueteturistico')),
            ],
        ),
    ]
