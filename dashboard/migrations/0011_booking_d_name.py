# Generated by Django 2.1.5 on 2019-03-02 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='d_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
