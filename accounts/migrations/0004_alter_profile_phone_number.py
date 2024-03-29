# Generated by Django 4.2.6 on 2024-01-25 21:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+201234567890'. Up to 13 digits allowed and only E.G phone accept.", regex='^\\+?120\\d{9,11}$')]),
        ),
    ]
