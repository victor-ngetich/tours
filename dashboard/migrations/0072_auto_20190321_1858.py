# Generated by Django 2.1.7 on 2019-03-21 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0071_auto_20190320_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='pricep_adult',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
