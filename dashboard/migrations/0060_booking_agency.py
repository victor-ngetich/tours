# Generated by Django 2.1.7 on 2019-03-17 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0059_package_agency'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='agency',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
