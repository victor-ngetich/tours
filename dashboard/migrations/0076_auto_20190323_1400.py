# Generated by Django 2.1.7 on 2019-03-23 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0075_auto_20190323_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='From'),
        ),
    ]
