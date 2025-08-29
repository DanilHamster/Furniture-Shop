from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Color(models.Model):
    color = models.CharField(max_length=25)

    class Meta:
        app_label = "service"

    def __str__(self):
        return f"{self.color}"


class Material(models.Model):
    material = models.CharField(max_length=25)

    class Meta:
        app_label = "service"

    def __str__(self):
        return f"{self.material}"


class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        validators=[
            MinValueValidator(0.99),
        ],
        decimal_places=2,
        max_digits=7,
    )
    description = models.CharField(null=True, blank=True, max_length=255)
    color = models.ForeignKey(
        Color, related_name="item_color", on_delete=models.CASCADE
    )
    material = models.ManyToManyField(Material, related_name="item_material")
    count = models.PositiveIntegerField(verbose_name="Count of item")
    item_class = models.ForeignKey(
        "ItemClass", on_delete=models.CASCADE, related_name="item_class"
    )
    image = models.ImageField(null=True, blank=True, upload_to="items/itemphoto/")
    comment = models.ManyToManyField("account.Comment", related_name="items")

    class Meta:
        app_label = "service"

    def get_image_url(self):
        if self.image:
            return self.image.url
        return f"{settings.STATIC_URL}img/placeholder.png"

    def __str__(self):
        return f"Item: {self.name}, Price: {self.price}"


class ItemClass(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = "service"

    def __str__(self):
        return f"{self.name}"
