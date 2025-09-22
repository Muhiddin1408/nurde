from django.urls import path

from payment.views.add_card import AddCardView
from payment.views.payme import payme_callback

urlpatterns = [

    path('payme/callback/', payme_callback, name='payme-callback'),
    path('add/card/', AddCardView.as_view(), name='add-card'),

]