# Generated by Django 2.1.7 on 2019-03-19 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0069_auto_20190319_0852'),
    ]

    operations = [
        migrations.RenameField(
            model_name='package',
            old_name='availabile',
            new_name='available',
        ),
    ]
