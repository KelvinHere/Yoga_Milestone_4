from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('user', 'order_number', 'date', 'discount',
                       'order_total', 'grand_total',)

    fields = ('user', 'order_number', 'date', 'full_name', 'email',
              'order_total', 'discount', 'grand_total',)

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)