# Generated by Django 3.2.8 on 2021-12-24 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tomato', '0007_basepricemanege'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basepricemanege',
            name='ratio',
            field=models.DecimalField(decimal_places=4, max_digits=5),
        ),
    ]