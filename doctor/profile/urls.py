from django.urls import path

from doctor.profile.views.edu import EducationListCreateView, EducationRetrieveUpdateDestroyView

urlpatterns = [
    path('educations/', EducationListCreateView.as_view(), name='education-list-create'),
    path('educations/<int:pk>/', EducationRetrieveUpdateDestroyView.as_view(), name='education-detail'),
]