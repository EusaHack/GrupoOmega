# Generated by Django 4.2.9 on 2024-11-25 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0015_remove_pagina_color_letra_pagina_color_letra_titulo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagina',
            name='color_letra_titulo_dos',
            field=models.CharField(default='#ffffff', max_length=8),
        ),
    ]
