# Generated by Django 4.2.8 on 2023-12-15 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_user_status_dcount_statususer_status_count'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StatusUser',
        ),
    ]
