from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken

from apps.basic.models import Specialist
from apps.users.model import Patient
from apps.users.models import User


def send_sms(mail, text):
    email = EmailMessage('Veri', text, to=[mail])
    email.send()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh = refresh
    access = refresh.access_token
    return str(refresh), str(access)

def register_social_user(email, name='',last = '', provider='email'):
    user = User.objects.filter(email=email).first()

    if user:
        return user
    else:
        user = {
            'email': email,
            'username': 'u' + email,
            'first_name': name,
            'last_name': last,
            'is_active': True
        }
        user = User.objects.create(**user)
        p = {
            'user': user,
        }
        Patient.objects.create(**p)
        return user
def register_social_doctor(email, name='',last = '', provider='email'):
    user = User.objects.filter(email=email).first()

    if user:
        return user
    else:
        user = {
            'email': email,
            'username': 'd' + email,
            'first_name': name,
            'last_name': last,
            'is_active': True
        }
        user = User.objects.create(**user)
        p = {
            'user': user,
        }
        Specialist.objects.create(**p)
        return user
