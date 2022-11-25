from django.contrib import admin

from service.models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(Item, ItemAdmin)
