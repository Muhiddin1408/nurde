from django.urls import path

from api.order.views.order import OrderViewSet

urlpatterns = [
    path('', OrderViewSet.as_view(), name='order'),
]