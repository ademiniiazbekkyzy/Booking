import time
from django.core.mail import send_mail
from .celery import app


@app.task
def send_mail_message(code, email, status):
    time.sleep(5)
    link = f'http://localhost:8000/account/activate/{code}'

    if status == 'register':

        send_mail(
            'From django project',
            link,
            'ademi.niiazbekkyzy@gmail.com',
            [email]
        )
    elif status == 'reset_password':
        send_mail(
            'Reset your password',
            f'Code activations: {code}',
            'stackoverflow@gmail.com',
            [email]
        )
    elif status == 'reserv':
        send_mail(
            'From django project',
            link,
            'ademi.niiazbekkyzy@gmail.com',
            [email]
        )


