from django.contrib import admin
from .models import Category, Product, Banner, Wishlist, SellerRequest


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge_text', 'badge_color', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'badge_color')
    search_fields = ('title', 'subtitle')
    ordering = ('order',)
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'image')
        }),
        ('Call-to-Action', {
            'fields': ('button_text', 'button_url', 'badge_text', 'badge_color')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active')
    list_editable = ('price', 'stock', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')


@admin.register(SellerRequest)
class SellerRequestAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'phone', 'approved', 'created_at')
    list_editable = ('approved',)
    list_filter = ('approved', 'created_at')
    search_fields = ('store_name', 'user__username', 'phone')
