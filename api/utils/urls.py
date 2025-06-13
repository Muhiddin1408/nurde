from django.urls import path

from api.utils.story import StoryListView
from api.utils.views.excel import symbtom
from api.utils.views.payme import payme_api
from api.utils.views.recomment import comment
from api.utils.views.image import ImageViewSet

urlpatterns = [
    path('comment/', comment, name='comment'),
    path('payme/', payme_api, name='payme_api'),
    path('stories/', StoryListView.as_view(), name='story_list'),
    path('symbtom/', symbtom, name='symbtomsss')
]