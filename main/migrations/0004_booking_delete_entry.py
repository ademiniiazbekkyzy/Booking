# Generated by Django 4.1.3 on 2022-12-10 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_entry_remove_checkout_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_time', models.DateTimeField(auto_now_add=True)),
                ('time_slot', models.IntegerField(choices=[(0, '09:00 - 10:00'), (1, '10:00 - 11:00'), (2, '11:00 - 12:00'), (3, '12:00 - 13:00'), (4, '14:00 - 15:00'), (5, '15:00 - 16:00'), (6, '16:00 - 17:00'), (7, '17:00 - 18:00')])),
                ('date', models.DateField(help_text='YYYY-MM-DD')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='main.element')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Entry',
        ),
    ]