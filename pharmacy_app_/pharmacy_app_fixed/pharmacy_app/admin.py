from django.contrib import admin
from .models import Medicine
from .models import Order, OrderItem


admin.site.register(Medicine)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'user', 'order_date', 'total_amount']

admin.site.register(Order, OrderAdmin)

