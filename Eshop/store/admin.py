from django.contrib import admin
from .models import *



# Register your models here.
admin.site.register(Category)
admin.site.register(customer)
admin.site.register(Order)
admin.site.register(OrderNumber)
admin.site.register(Product)
# class AdminProduct(admin.ModelAdmin):
#     list_display = ['name', 'price', 'category']
#
#
# class AdminCategory(admin.ModelAdmin):
#     list_display = ['name']
#
# class Admincustomer(admin.ModelAdmin):
#     list_display = ['first_name','email']
#
# class AdminORDER(admin.ModelAdmin):
#     list_display = ['id','customer','product']
#
# class AdminORDERNumber(admin.ModelAdmin):
#     list_display = ['id','amount']


# admin.site.register(Product, AdminProduct)
# admin.site.register(Category,AdminCategory)
# admin.site.register(customer,Admincustomer)
# admin.site.register(Order,AdminORDER)
# admin.site.register(OrderNumber,AdminORDERNumber)