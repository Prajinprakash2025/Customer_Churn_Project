from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = "Assign existing demo images to demo products."

    def handle(self, *args, **options):
        # Map demo product names to existing image files in media/products
        name_to_image = {
            "Samsung Galaxy S24": "phone.jpg",
            "iPhone 15 Pro": "phone_fOdJmap.jpg",
            "Dell XPS 13": "ASUS.png",
            "MacBook Air M2": "ASUS.png",
            "Logitech MX Master 3S Mouse": "bag.jpg",
            "Sony WH-1000XM5 Headphones": "bag.jpg",
            "LG 1.5 Ton Inverter AC": "ASUS.png",
            "Samsung 7kg Front Load Washing Machine": "ASUS.png",
        }

        updated_count = 0

        for product_name, filename in name_to_image.items():
            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                continue

            # Only set image if it's currently empty
            if not product.image:
                product.image = f"products/{filename}"
                product.save(update_fields=["image"])
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Assigned demo images to {updated_count} product(s)."
            )
        )

