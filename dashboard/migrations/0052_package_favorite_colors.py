# Generated by Django 2.1.7 on 2019-03-06 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0051_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='favorite_colors',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
