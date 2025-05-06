from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken

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

def register_social_user(email, name='', provider='email'):
    user = User.objects.filter(email=email).first()


    if user:
        return user
    else:
        user = {
            'email': email,
            'username': 'u' + email,
            'first_name': name,
            'auth_provider': provider,
            'is_active': True
        }
        user = User.objects.create(**user)
        p = {
            'user': user,
        }
        Patient.objects.create(**p)
        return user
