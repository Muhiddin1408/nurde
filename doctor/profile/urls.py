from django.urls import path

from doctor.profile.views.edu import EducationListCreateView, EducationRetrieveUpdateDestroyView
from doctor.profile.views.order import OrderView, OrderDetailView

urlpatterns = [
    path('educations/', EducationListCreateView.as_view(), name='education-list-create'),
    path('educations/<int:pk>/', EducationRetrieveUpdateDestroyView.as_view(), name='education-detail'),
    path('order/', OrderView.as_view(), name='order'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]