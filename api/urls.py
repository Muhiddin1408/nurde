from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('clinic/', include('api.clinic.urls'), name='clinic'),
    path('laboratory/', include('api.labaratory.urls')),
    path('specialist/', include('api.basic.urls'), name='specialist'),
    path('symptom/', include('api.symptom.urls'), name='symptom'),
    path('order/', include('api.order.urls'), name='order'),
    path('utils/', include('api.utils.urls'), name='utils'),
    path('users/', include('api.users.urls'), name='users'),

]