# Generated by Django 3.1.7 on 2024-06-07 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0016_auto_20240606_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='paqueteturistico',
            name='imagen',
            field=models.ImageField(null=True, upload_to='imagenes/'),
        ),
        migrations.DeleteModel(
            name='Imagen',
        ),
    ]
