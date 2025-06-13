from django.urls import path

from .views import PaymeCallBackAPIView

urlpatterns = [

    path("payment/update/", PaymeCallBackAPIView.as_view()),

]