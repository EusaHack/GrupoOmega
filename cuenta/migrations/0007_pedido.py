# Generated by Django 4.2.9 on 2024-11-10 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0006_producto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('estado_entrega', models.CharField(choices=[('pendiente', 'Pendiente'), ('entregado', 'Entregado')], default='pendiente', max_length=10)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuenta.producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
