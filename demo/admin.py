from django.contrib import admin

# Register your models here.
from demo.forms import OrderForm
from demo.models import *


class ItemInOrder(admin.TabularInline):
    model = ItemInOrder


class AdminOrder(admin.ModelAdmin):
    form = OrderForm
    list_display = ('date', 'user', 'count_product')
    list_filter = ('status',)
    fields = ('status', 'rejection_reason')
    inlines = (ItemInOrder,)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order, AdminOrder)