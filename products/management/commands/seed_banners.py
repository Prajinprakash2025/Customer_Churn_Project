from django.core.management.base import BaseCommand
from django.core.files import File
import os


class Command(BaseCommand):
    help = "Seed default banner images into the Banner model"

    def handle(self, *args, **kwargs):
        from products.models import Banner

        MEDIA_ROOT = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
            "media", "banners"
        )

        banners_data = [
            {
                "title": "Summer Sale\nUp to 70% OFF",
                "subtitle": "Hottest deals on electronics, fashion & more",
                "image_file": "banner_summer.png",
                "button_text": "Shop Now →",
                "button_url": "/",
                "badge_text": "Limited Time",
                "badge_color": "orange",
                "order": 1,
            },
            {
                "title": "Tech &\nElectronics",
                "subtitle": "Latest gadgets at unbeatable prices",
                "image_file": "banner_electronics.png",
                "button_text": "Explore →",
                "button_url": "/",
                "badge_text": "New Arrivals",
                "badge_color": "blue",
                "order": 2,
            },
            {
                "title": "Trendy Styles\nJust for You",
                "subtitle": "Clothing, bags & accessories at great prices",
                "image_file": "banner_fashion.png",
                "button_text": "Shop Fashion →",
                "button_url": "/",
                "badge_text": "Fashion Week",
                "badge_color": "pink",
                "order": 3,
            },
            {
                "title": "Beautiful\nHome Decor",
                "subtitle": "Transform your living space today",
                "image_file": "banner_home.png",
                "button_text": "Discover →",
                "button_url": "/",
                "badge_text": "Home Essentials",
                "badge_color": "green",
                "order": 4,
            },
        ]

        created = 0
        for data in banners_data:
            image_path = os.path.join(MEDIA_ROOT, data["image_file"])
            if not os.path.exists(image_path):
                self.stdout.write(self.style.WARNING(
                    f"  ⚠ Image not found: {image_path} — skipping '{data['title']}'"
                ))
                continue

            if not Banner.objects.filter(title=data["title"]).exists():
                banner = Banner(
                    title=data["title"],
                    subtitle=data["subtitle"],
                    button_text=data["button_text"],
                    button_url=data["button_url"],
                    badge_text=data["badge_text"],
                    badge_color=data["badge_color"],
                    order=data["order"],
                    is_active=True,
                )
                with open(image_path, "rb") as f:
                    banner.image.save(data["image_file"], File(f), save=True)
                created += 1
                self.stdout.write(self.style.SUCCESS(f"  ✅ Created banner: {data['title'].splitlines()[0]}"))
            else:
                self.stdout.write(f"  — Banner already exists: {data['title'].splitlines()[0]}")

        self.stdout.write(self.style.SUCCESS(f"\nDone. {created} banner(s) created."))
