# Generated by Django 4.2.6 on 2024-02-12 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
