from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Feedback)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'price', 'tags', 'image', 'created']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class ShippingAddressInline(admin.TabularInline):
    model = ShippingAddress
    extra = 0
    exclude = ['customer']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date_ordered', 'complete', 'status']
    inlines = [OrderItemInline, ShippingAddressInline]


admin.site.register(Order, OrderAdmin)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'created', 'is_read']


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['customer', 'date_ordered', 'complete', 'status']
#
#
# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['order', 'product', 'quantity', 'date_added']
#
#
# @admin.register(ShippingAddress)
# class ShippingAddressAdmin(admin.ModelAdmin):
#     list_display = ['customer', 'address', 'city', 'division']
