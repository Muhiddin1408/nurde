from django.urls import path

from api.order.views.order import OrderViewSet, ImageViewSet

urlpatterns = [
    path('', OrderViewSet.as_view(), name='order'),
    path('image/', ImageViewSet.as_view(), name='image'),
]