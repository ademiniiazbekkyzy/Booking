from django.core.mail import send_mail


def send_activation_code(email, activation_code):
    activation_url = f'http://localhost:8000/v1/api/account/activate/{activation_code}'
    message = f"Thank you for signing up! Activation link : {activation_url}"

    send_mail(
        'From django project',
        message,
        'ademi.niiazbekkyzy@gmail.com',
        [email, ]
    )