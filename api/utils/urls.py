from django.urls import path

from api.utils.views.recomment import comment
from api.utils.views.image import ImageViewSet

urlpatterns = [
    path('comment/', comment, name='comment'),
]