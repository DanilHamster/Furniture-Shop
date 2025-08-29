from django.contrib import admin

from service.models import Item, Color, Material, ItemClass

admin.site.register(Item)
admin.site.register(Color)
admin.site.register(Material)
admin.site.register(ItemClass)
