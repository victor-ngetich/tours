# Generated by Django 2.1.7 on 2019-03-16 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0058_auto_20190315_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='agency',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
