from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","first_name","phone","payment_method","delivery_method","paid","created_at")
    list_filter  = ("paid","payment_method","delivery_method","created_at")
    inlines = [OrderItemInline]