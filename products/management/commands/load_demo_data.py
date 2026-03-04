from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = "Load demo categories and products for the ecommerce site."

    def handle(self, *args, **options):
        demo_categories = [
            "Laptops",
            "Smartphones",
            "Accessories",
            "Home Appliances",
        ]

        category_objects = {}
        for name in demo_categories:
            category, _ = Category.objects.get_or_create(name=name)
            category_objects[name] = category

        demo_products = [
            {
                "category": "Laptops",
                "name": "MacBook Air M2",
                "price": 115000,
                "stock": 15,
                "description": "13-inch Apple MacBook Air with M2 chip, 8GB RAM, 256GB SSD.",
            },
            {
                "category": "Laptops",
                "name": "Dell XPS 13",
                "price": 98000,
                "stock": 10,
                "description": "Premium ultrabook with Intel i7, 16GB RAM, 512GB SSD.",
            },
            {
                "category": "Smartphones",
                "name": "iPhone 15 Pro",
                "price": 135000,
                "stock": 25,
                "description": "Apple iPhone 15 Pro with A17 chip and 256GB storage.",
            },
            {
                "category": "Smartphones",
                "name": "Samsung Galaxy S24",
                "price": 105000,
                "stock": 30,
                "description": "Flagship Android phone with Dynamic AMOLED display.",
            },
            {
                "category": "Accessories",
                "name": "Logitech MX Master 3S Mouse",
                "price": 9500,
                "stock": 50,
                "description": "Ergonomic wireless mouse for productivity.",
            },
            {
                "category": "Accessories",
                "name": "Sony WH-1000XM5 Headphones",
                "price": 29000,
                "stock": 20,
                "description": "Wireless noise-cancelling over-ear headphones.",
            },
            {
                "category": "Home Appliances",
                "name": "LG 1.5 Ton Inverter AC",
                "price": 42000,
                "stock": 12,
                "description": "Energy-efficient split AC suitable for medium rooms.",
            },
            {
                "category": "Home Appliances",
                "name": "Samsung 7kg Front Load Washing Machine",
                "price": 38000,
                "stock": 8,
                "description": "Fully-automatic front load washer with eco bubble.",
            },
        ]

        created_count = 0

        for item in demo_products:
            category = category_objects.get(item["category"])
            if not category:
                continue

            product, created = Product.objects.get_or_create(
                name=item["name"],
                defaults={
                    "category": category,
                    "price": item["price"],
                    "stock": item["stock"],
                    "description": item["description"],
                    "is_active": True,
                },
            )

            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo data loaded successfully. Products created: {created_count}"
            )
        )

