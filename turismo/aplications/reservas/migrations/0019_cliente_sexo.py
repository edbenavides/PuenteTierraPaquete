# Generated by Django 3.1.7 on 2024-06-18 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0018_auto_20240606_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='sexo',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
    ]
