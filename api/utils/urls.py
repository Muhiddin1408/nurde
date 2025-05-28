from django.urls import path

from api.utils.views.payme import payme_api
from api.utils.views.recomment import comment
from api.utils.views.image import ImageViewSet

urlpatterns = [
    path('comment/', comment, name='comment'),
    path('payme/', payme_api, name='payme_api'),
]