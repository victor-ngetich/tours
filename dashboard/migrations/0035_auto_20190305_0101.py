# Generated by Django 2.1.7 on 2019-03-04 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0034_auto_20190305_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='d_description',
            field=models.CharField(blank=True, max_length=16383),
        ),
    ]
