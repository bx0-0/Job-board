# Generated by Django 4.2.6 on 2024-02-16 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_alter_profile_is_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_company',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
