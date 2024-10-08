# Generated by Django 2.2.7 on 2019-11-04 14:48

import dashboard.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_name', models.CharField(blank=True, max_length=255, verbose_name='Destination')),
                ('agency', models.CharField(blank=True, max_length=255, verbose_name='Agency')),
                ('agencyname', models.CharField(blank=True, max_length=255, verbose_name='Travel Agency')),
                ('agencyemail', models.CharField(blank=True, max_length=255, verbose_name='Agency Email')),
                ('agencycontact', models.CharField(blank=True, max_length=255, verbose_name='Agency Contact')),
                ('user_full', models.CharField(blank=True, max_length=255, verbose_name='Client')),
                ('clientemail', models.CharField(blank=True, max_length=255, verbose_name="Client's Email")),
                ('adults', models.IntegerField(blank=True, default=1, verbose_name='Adults')),
                ('kids', models.IntegerField(blank=True, default=0, verbose_name='Kids')),
                ('pricep_adult', models.FloatField(blank=True, default=0, verbose_name='Price per Adult')),
                ('pricep_kid', models.FloatField(blank=True, default=0, verbose_name='Price per Kid')),
                ('days', models.IntegerField(blank=True, default=1, verbose_name='Days')),
                ('start_date', models.DateField(blank=True, default=datetime.date.today, null=True, validators=[dashboard.models.validate_date], verbose_name='From')),
                ('end_date', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='To')),
                ('approved', models.BooleanField(default=False, verbose_name='Approved?')),
                ('paid', models.BooleanField(default=False, verbose_name='Paid?')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Booked')),
            ],
            options={
                'ordering': ('-date_added',),
            },
        ),
        migrations.CreateModel(
            name='destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_name', models.CharField(blank=True, max_length=255, verbose_name='Destination')),
                ('d_location', models.CharField(blank=True, max_length=255, verbose_name='Location')),
                ('d_description', models.TextField(blank=True, verbose_name='Description')),
                ('d_pic1', models.FileField(blank=True, upload_to='dashboard/', verbose_name='Pic 1')),
                ('d_pic2', models.FileField(blank=True, upload_to='dashboard/', verbose_name='Pic 2')),
                ('d_pic3', models.FileField(blank=True, upload_to='dashboard/', verbose_name='Pic 3')),
                ('d_phone', models.CharField(blank=True, max_length=15, verbose_name='Phone')),
                ('d_email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('d_reviews', models.CharField(blank=True, max_length=255, verbose_name='Reviews')),
                ('d_uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
            ],
            options={
                'ordering': ('d_name',),
            },
        ),
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency', models.CharField(blank=True, max_length=255, verbose_name='Agency')),
                ('agencyname', models.CharField(blank=True, max_length=255, verbose_name='Travel Agency')),
                ('agencyemail', models.CharField(blank=True, max_length=255, verbose_name='Agency Email')),
                ('agencycontact', models.CharField(blank=True, max_length=255, verbose_name='Agency Contact')),
                ('user_full', models.CharField(blank=True, max_length=255, verbose_name='Client')),
                ('clientemail', models.CharField(blank=True, max_length=255, verbose_name='Email')),
                ('amountpaid', models.FloatField(blank=True, default=0, verbose_name='Amount Paid ($USD)')),
                ('transaction_status', models.CharField(blank=True, max_length=255, verbose_name='Transaction Status')),
                ('transaction_id', models.CharField(blank=True, max_length=255, unique=True, verbose_name='Transaction ID')),
                ('hotel', models.CharField(blank=True, max_length=255, verbose_name='Preferred Hotel')),
                ('adults', models.IntegerField(blank=True, default=1, verbose_name='Adults')),
                ('kids', models.IntegerField(blank=True, default=0, verbose_name='Kids')),
                ('pricep_adult', models.FloatField(blank=True, default=0, verbose_name='Price per Adult')),
                ('pricep_kid', models.FloatField(blank=True, default=0, verbose_name='Price per Kid')),
                ('days', models.IntegerField(blank=True, default=1, verbose_name='Days')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='From')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='To')),
                ('date_added', models.DateTimeField(blank=True, verbose_name='Date Booked')),
                ('date_paid', models.DateTimeField(auto_now_add=True, verbose_name='Date Paid')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.booking', verbose_name='Package')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Client')),
            ],
        ),
        migrations.CreateModel(
            name='package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(blank=True, max_length=255, verbose_name='Package Name')),
                ('p_category', models.CharField(blank=True, choices=[('Beaches', 'Beaches'), ('Bike Rides', 'Bike Rides'), ('Heritage', 'Heritage'), ('Hot Air Ballooning', 'Hot Air Ballooning'), ('Museums', 'Museums'), ('Resorts', 'Resorts'), ('Road Trips', 'Road Trips'), ('Scenery', 'Scenery'), ('Vacation Rentals', 'Vacation Rentals'), ('Wildlife', 'Wildlife')], max_length=255, verbose_name='Category')),
                ('p_agency', models.CharField(blank=True, max_length=255, verbose_name='Travel Agency')),
                ('agencyemail', models.CharField(blank=True, max_length=255, verbose_name='Agency Email')),
                ('agency_phone', models.CharField(blank=True, max_length=10, verbose_name='Phone')),
                ('pricep_adult', models.FloatField(blank=True, default=0, verbose_name='Price per Adult')),
                ('pricep_kid', models.FloatField(blank=True, default=0, verbose_name='Price per Kid')),
                ('p_description', models.TextField(blank=True, verbose_name='Description')),
                ('from_day', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='From')),
                ('to_day', models.DateField(blank=True, default=dashboard.models.one_month_from_today, null=True, verbose_name='To')),
                ('p_slots', models.IntegerField(blank=True, default=0, verbose_name='Number Slots')),
                ('available', models.BooleanField(default=True, verbose_name='Available?')),
                ('agency', models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Agency')),
                ('d_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.destination', verbose_name='Destination')),
            ],
            options={
                'ordering': ('p_name', 'd_name'),
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('h_name', models.CharField(blank=True, max_length=255, verbose_name='Hotel')),
                ('pricep_adult', models.FloatField(blank=True, default=0, verbose_name='Price per Adult')),
                ('pricep_kid', models.FloatField(blank=True, default=0, verbose_name='Price per Kid')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.destination', verbose_name='Destination')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Hotel', verbose_name='Hotel'),
        ),
        migrations.AddField(
            model_name='booking',
            name='p_name2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.package', verbose_name='Package'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Client'),
        ),
    ]
