from django.contrib import admin

from service.models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')


admin.site.register(Item, ItemAdmin)
