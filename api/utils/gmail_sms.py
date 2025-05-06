from django.core.mail import EmailMessage


def send_sms(mail, text):
    email = EmailMessage('Veri', text, to=[mail])
    email.send()