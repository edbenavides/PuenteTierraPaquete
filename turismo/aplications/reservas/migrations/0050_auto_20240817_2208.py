# Generated by Django 3.1.7 on 2024-08-18 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0049_auto_20240817_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fechasreserva',
            name='fechaFinal',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='fechasreserva',
            name='fechaInicio',
            field=models.DateField(),
        ),
    ]
