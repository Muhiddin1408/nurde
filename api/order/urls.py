from django.urls import path
from rest_framework.routers import SimpleRouter

from api.order.views.order import OrderViewSet, ImageViewSet, MyOrderViewSet

router = SimpleRouter()
router.register('my', MyOrderViewSet, basename='my')

urlpatterns = [
    path('', OrderViewSet.as_view(), name='order'),
    path('image/', ImageViewSet.as_view(), name='image'),
] + router.urls