# Generated by Django 2.1.7 on 2019-03-04 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_auto_20190305_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='d_description',
            field=models.TextField(blank=True, max_length=16383),
        ),
    ]
