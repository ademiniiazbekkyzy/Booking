# Generated by Django 4.1.3 on 2022-12-10 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_booking_delete_entry'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='phone',
            field=models.CharField(default='-', max_length=30),
        ),
    ]
