# Generated by Django 3.1.7 on 2024-06-19 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0027_auto_20240618_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
    ]
