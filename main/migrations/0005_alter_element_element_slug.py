# Generated by Django 4.1.3 on 2022-12-05 17:12

from django.db import migrations, models
import main.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_reservation_checking_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='element_slug',
            field=models.SlugField(default=main.models.Element),
        ),
    ]
