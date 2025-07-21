from django.contrib import admin
from .models import ProductType, Department, Product, Vendor, Purchase, Customer, Sell
# Register your models here.


admin.site.register(ProductType)
admin.site.register(Department)
admin.site.register(Product)
admin.site.register(Vendor)
admin.site.register(Purchase)
admin.site.register(Customer)
admin.site.register(Sell)
