from django.urls import path

from doctor.profile.views.category import CategoryListView
from doctor.profile.views.chat import MessageViewSet
from doctor.profile.views.edu import EducationListCreateView, EducationRetrieveUpdateDestroyView, \
    FileEducationListCreateView
from doctor.profile.views.order import OrderView, OrderDetailView, confirm, close
from doctor.profile.views.ranking import RankingView, CommentView
from doctor.profile.views.schedule import MyScheduleView, WeekdayView
from doctor.profile.views.service import ServiceViewSet, ServiceDetail, MyCategoryViewSet
from doctor.profile.views.work import WorkListCreateView, WorkRetrieveUpdateDestroyView, FileWorkListCreateView

urlpatterns = [
    path('educations/', EducationListCreateView.as_view(), name='education-list-create'),
    path('educations/<int:pk>/', EducationRetrieveUpdateDestroyView.as_view(), name='education-detail'),
    path('edu/file/', FileEducationListCreateView.as_view(), name='education-file-list-create'),
    path('works/', WorkListCreateView.as_view(), name='work-list-create'),
    path('work/<int:pk>/', WorkRetrieveUpdateDestroyView.as_view(), name='work-detail'),
    path('work/file/', FileWorkListCreateView.as_view(), name='work-file-list-create'),
    path('order/', OrderView.as_view(), name='order'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('confirm/', confirm),
    path('order/close/', close),
    path('category/', CategoryListView.as_view(), name='category-list'),
    path('my/category/', MyCategoryViewSet.as_view(), name='my-category-list'),
    path('chat/', MessageViewSet.as_view(), name='chat_doctor'),
    path('ranking/', RankingView.as_view(), name='ranking'),
    path('comment/', CommentView.as_view()),
    path('service/', ServiceViewSet.as_view(), name='service'),
    path('service/<int:pk>/', ServiceDetail.as_view(), name='update-service'),
    path('my/schedule/', MyScheduleView.as_view(), name='my-schedule'),
    path('weekday/', WeekdayView.as_view(), name='weekday'),
]