from tkinter.constants import CASCADE

from django.contrib.auth.models import AbstractUser
from django.db import models

from service.models import Item


class LastBuyItem(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="last_buys")
    item_name = models.CharField(max_length=128, null=True)
    price_was = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    bought_at = models.DateTimeField(auto_now_add=True)
    item_id = models.IntegerField()

    def __str__(self):
        return f"{self.item_name} x{self.quantity} @ {self.bought_at:%Y-%m-%d %H:%M}"

    @property
    def get_total_price(self):
        return self.price_was * self.quantity


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=64)
    avatar = models.ImageField(
        null=True, blank=True, upload_to="accounts/profiles/avatars/"
    )

    def get_image_url(self):
        if self.avatar:
            return self.avatar.url
        return "/static/img/placeholder.png"


class Comment(models.Model):
    text = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    create = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_price(self):
        return sum(
            cart_item.quantity * cart_item.item.price
            for cart_item in self.items.select_related("item")
        )


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["cart", "item"], name="unique_cart_item")
        ]

    def __str__(self):
        return f"Sum for {self.quantity} × {self.item.name}: ${self.quantity * self.item.price:.2f}"


class Buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.IntegerField()
    item_quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=30)
    card_number = models.CharField(max_length=30)
    cvv = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    @property
    def get_total_price(self):
        return self.item_price * self.item_quantity
