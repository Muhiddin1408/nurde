from django.urls import path, include

urlpatterns = [
    path('auth/', include('doctor.auth.urls'))
]