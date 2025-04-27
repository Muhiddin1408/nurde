from django.urls import path
from rest_framework.routers import SimpleRouter

from api.order.views.order import OrderViewSet, ImageViewSet, MyOrderViewSet, DiagnosisViewSet

router = SimpleRouter()
router.register('my', MyOrderViewSet, basename='my')
router.register('diagnosis', DiagnosisViewSet, basename='diagnosis')

urlpatterns = [
    path('', OrderViewSet.as_view(), name='order'),
    path('image/', ImageViewSet.as_view(), name='image'),
] + router.urls