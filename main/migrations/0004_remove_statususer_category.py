# Generated by Django 4.2.8 on 2023-12-15 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_statususer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statususer',
            name='category',
        ),
    ]
