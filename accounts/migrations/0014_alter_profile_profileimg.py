# Generated by Django 4.2.6 on 2024-02-14 13:44

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_profile_unconfirmed_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ProfileImg',
            field=models.ImageField(default=1, upload_to=accounts.models.GetImageUploadTo),
            preserve_default=False,
        ),
    ]
