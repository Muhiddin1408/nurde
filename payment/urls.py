from django.urls import path

from payment.views.payme import payme_callback

urlpatterns = [

    path('payme/callback/', payme_callback, name='payme-callback')

]