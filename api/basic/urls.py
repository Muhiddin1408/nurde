from django.urls import path
from rest_framework.routers import SimpleRouter

from api.basic.views.filter import filter_list
from api.basic.views.specialist import SpecialistViewSet, SpecialistCategoryViewSet

app_name = 'basic'

router = SimpleRouter()
router.register('category', SpecialistViewSet, basename='category')
router.register('specialists', SpecialistCategoryViewSet, basename='specialists')
urlpatterns = [
    path('filter/list/', filter_list, name='filter_list'),
] + router.urls
