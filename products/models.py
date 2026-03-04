from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=120)
    icon = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Banner(models.Model):
    """Hero carousel banner manageable from Django Admin."""
    BADGE_COLORS = [
        ('orange', 'Orange'),
        ('pink', 'Pink'),
        ('green', 'Green'),
        ('blue', 'Blue'),
        ('red', 'Red'),
        ('purple', 'Purple'),
    ]

    title = models.CharField(max_length=100, help_text="Main heading (can use line breaks with \\n)")
    subtitle = models.CharField(max_length=200, blank=True, default="", help_text="Sub-text under heading")
    image = models.ImageField(upload_to="banners/", help_text="Background image (recommended 1400x500px)")
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_url = models.CharField(max_length=200, default="/", help_text="URL for the CTA button")
    badge_text = models.CharField(max_length=40, blank=True, default="Sale", help_text="Small pill label above title")
    badge_color = models.CharField(max_length=10, choices=BADGE_COLORS, default='orange')
    order = models.PositiveSmallIntegerField(default=0, help_text="Lower number = shown first in carousel")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
