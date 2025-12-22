from django.contrib import admin
from .models import Products,Address,Order

# Register your models here.

admin.site.register(Products)
admin.site.register(Address)
admin.site.register(Order)
