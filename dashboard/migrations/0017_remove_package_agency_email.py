# Generated by Django 2.1.7 on 2019-03-03 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_destination_d_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='agency_email',
        ),
    ]
