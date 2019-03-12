# Generated by Django 2.1.7 on 2019-03-11 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0060_auto_20190309_1308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ('-date_added',)},
        ),
        migrations.RemoveField(
            model_name='package',
            name='favorite_colors',
        ),
        migrations.AddField(
            model_name='package',
            name='p_slots',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
