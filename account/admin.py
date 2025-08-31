from django.contrib import admin

from account.models import LastBuyItem, User, Comment, Cart, CartItem, Order

admin.site.register(LastBuyItem)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
