# Generated by Django 2.1.7 on 2019-03-04 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_auto_20190305_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='d_description',
            field=models.TextField(blank=True),
        ),
    ]
