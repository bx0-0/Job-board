# Generated by Django 4.2.6 on 2024-01-25 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('accounts', '0005_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.city'),
        ),
    ]
