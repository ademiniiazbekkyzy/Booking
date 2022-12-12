from celery import shared_task
from django.core.mail import send_mail
from booking_api.celery import app
from main.models import Booking


@app.task
def entry_created(entry_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    entry = Booking.objects.get(id=entry_id)
    subject = 'Appointment nr. {}'.format(entry_id)
    message = 'Dear {},\n\nYou have successfully made an appointment with Dr. {} by {} on {}'.format(entry.user.email,
                                             entry.doctor.last_name,
                                             entry.time,
                                             entry.date)
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [entry.user.email])
    return mail_sent