from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.auth.urls'), name='index'),
    path('clinic/', include('api.clinic.urls'), name='clinic'),
    path('specialist/', include('api.basic.urls'), name='specialist'),
]