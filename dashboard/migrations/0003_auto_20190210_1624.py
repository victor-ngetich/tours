# Generated by Django 2.1.5 on 2019-02-10 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20190210_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='category',
            field=models.CharField(blank=True, choices=[('0', 'Beaches'), ('1', 'Bike Rides'), ('2', 'Heritage'), ('3', 'Hot Air Ballooning'), ('4', 'Museums'), ('5', 'Resorts'), ('6', 'Road Trips'), ('7', 'Scenery'), ('8', 'Vacation Rentals'), ('9', 'Wildlife')], max_length=255),
        ),
    ]
