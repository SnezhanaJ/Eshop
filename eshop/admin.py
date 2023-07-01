from django.contrib import admin
from .models import *


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "category", ]
    list_filter = ["name", "price", "category", ]

    def has_add_permission(self, request):
        return True


admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)

