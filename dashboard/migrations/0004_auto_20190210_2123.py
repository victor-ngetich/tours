# Generated by Django 2.1.5 on 2019-02-10 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20190210_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='category',
            field=models.CharField(blank=True, choices=[('Beaches', 'Beaches'), ('Bike Rides', 'Bike Rides'), ('Heritage', 'Heritage'), ('Hot Air Ballooning', 'Hot Air Ballooning'), ('Museums', 'Museums'), ('Resorts', 'Resorts'), ('Road Trips', 'Road Trips'), ('Scenery', 'Scenery'), ('Vacation Rentals', 'Vacation Rentals'), ('Wildlife', 'Wildlife')], max_length=255),
        ),
        migrations.AlterField(
            model_name='destination',
            name='pics',
            field=models.FileField(blank=True, max_length=255, upload_to='dashboard/'),
        ),
    ]
