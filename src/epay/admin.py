from django.contrib import admin
from epay import models


class ProductAdmin (admin.ModelAdmin):
    list_display = ('__str__', 'price')


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Payee)
admin.site.register(models.Invoice)
