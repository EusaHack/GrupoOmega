# Generated by Django 4.2.9 on 2024-03-19 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0003_customuser_delete_product_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
