# Generated by Django 4.2.4 on 2024-04-08 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='open_seats',
        ),
    ]
