# Generated by Django 4.2.6 on 2024-01-30 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ProfileImg',
            field=models.ImageField(null=True, upload_to='profile/'),
        ),
    ]
