from django.contrib import admin

from apps.order.models import Order, OrderFile, Diagnosis, Recommendations

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderFile)
admin.site.register(Diagnosis)
admin.site.register(Recommendations)
