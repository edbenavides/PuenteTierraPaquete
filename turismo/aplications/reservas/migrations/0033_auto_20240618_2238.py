# Generated by Django 3.1.7 on 2024-06-19 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0032_auto_20240618_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cantidad',
            field=models.IntegerField(default=1, help_text='Coloque la cantidad de personas'),
        ),
    ]
