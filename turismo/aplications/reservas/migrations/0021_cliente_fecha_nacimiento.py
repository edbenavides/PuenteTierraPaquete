# Generated by Django 3.1.7 on 2024-06-18 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0020_remove_cliente_sexo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
