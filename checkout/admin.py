from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('profile', 'order_number', 'stripe_id',
                       'date', 'discount', 'order_total', 'grand_total',
                       'original_basket',)

    fields = ('profile', 'order_number', 'stripe_id', 'date',
              'full_name', 'email', 'order_total', 'discount',
              'grand_total', 'original_basket',)

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)