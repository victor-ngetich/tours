# Generated by Django 2.1.7 on 2019-03-12 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0072_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='hotel',
            field=models.ManyToManyField(to='dashboard.Hotel'),
        ),
    ]
