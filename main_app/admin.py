from django.contrib import admin

# Register your models here.
from main_app.models import Customer, Service, Order

admin.site.register(Customer)
admin.site.register(Service)
admin.site.register(Order)