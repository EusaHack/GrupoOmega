# Generated by Django 4.2.9 on 2024-11-26 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0016_alter_pagina_color_letra_titulo_dos'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagina',
            name='color_boton',
            field=models.CharField(default='#2b4e71', max_length=8),
        ),
        migrations.AddField(
            model_name='pagina',
            name='color_letra_boton',
            field=models.CharField(default='#ffff', max_length=8),
        ),
    ]