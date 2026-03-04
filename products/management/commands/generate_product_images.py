from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import os
import io

class Command(BaseCommand):
    help = "Generate placeholder images for all products"

    def handle(self, *args, **kwargs):
        from products.models import Product

        products = Product.objects.all()
        created = 0

        # Colors for placeholder backgrounds
        colors = ['#EFF6FF', '#F0FDF4', '#FEFCE8', '#FFF1F2', '#F8FAFC']
        
        for i, product in enumerate(products):
            # Create a 600x600 square image
            bg_color = colors[i % len(colors)]
            img = Image.new('RGB', (600, 600), color=bg_color)
            draw = ImageDraw.Draw(img)
            
            # Category text on top
            cat_name = product.category.name if product.category else "Product"
            cat_color = "#64748B"
            
            # Very simple text centering without external fonts
            # We'll just draw some rectangles or very basic shapes to look like a product,
            # and write the initials.
            
            # Draw a darker shape to represent the product
            shape_color = "#334155"
            draw.rounded_rectangle([150, 150, 450, 450], radius=20, fill=shape_color)
            
            # Simple "Product" initial
            initial = product.name[0].upper() if product.name else "P"
            
            try:
                # Try to use a default truetype font if available
                # Windows might have arial
                font = ImageFont.truetype("arial.ttf", 150)
            except IOError:
                # Fallback to default bitmap font
                font = ImageFont.load_default()
            
            # Center the initial approx
            draw.text((300, 300), initial, fill="white", font=font, anchor="mm")
            
            # Add full product name at bottom
            try:
                small_font = ImageFont.truetype("arial.ttf", 30)
            except IOError:
                small_font = ImageFont.load_default()
            
            draw.text((300, 520), product.name[:30], fill="#0F172A", font=small_font, anchor="mm")
            draw.text((300, 80), cat_name, fill="#64748B", font=small_font, anchor="mm")
            
            # Save to memory
            blob = io.BytesIO()
            img.save(blob, 'PNG')
            
            # Save to product
            filename = f"product_{product.id}_placeholder.png"
            product.image.save(filename, File(blob), save=True)
            created += 1
            
            self.stdout.write(f"Updated {product.name} with placeholder.")
            
        self.stdout.write(self.style.SUCCESS(f"Successfully generated images for {created} products."))
