"""Populate the database with demo content for local development.

Idempotent: running it more than once will not create duplicates. It also
creates a superuser (credentials configurable via the DJANGO_SUPERUSER_*
environment variables, defaulting to admin/admin for local use only).

Usage:
    python manage.py seed_demo
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from contactinfo.models import Contactinfo
from webpages.models import Slider, Team
from youtubers.models import Youtuber


class Command(BaseCommand):
    help = "Seed the database with demo content (idempotent)."

    def handle(self, *args, **options):
        self._create_superuser()
        self._create_contactinfo()
        self._create_sliders()
        self._create_team()
        self._create_youtubers()
        self.stdout.write(self.style.SUCCESS("Demo data seeded."))

    # -- helpers ---------------------------------------------------------

    def _create_superuser(self):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(f"  created superuser '{username}' (password: '{password}')")
        else:
            self.stdout.write(f"  superuser '{username}' already exists")

    def _create_contactinfo(self):
        if Contactinfo.objects.exists():
            self.stdout.write("  contactinfo already present")
            return
        Contactinfo.objects.create(
            first_name="AdTubers",
            last_name="Team",
            fb_handle="https://facebook.com/adtubers",
            insta_handle="https://instagram.com/adtubers",
            youtube_handle="https://youtube.com/@adtubers",
            twitter_handle="https://twitter.com/adtubers",
            description_1="AdTubers connects content creators with event organizers.",
            description_2="Find the perfect creator for your next event.",
            phone="9876543210",
            email="hello@adtubers.example.com",
        )
        self.stdout.write("  created contactinfo")

    def _create_sliders(self):
        sliders = [
            ("Hire the best content creators", "Bridge between creators and events",
             "Explore Tubers", "slider/2021/banner1.png"),
            ("Grow your brand with creators", "Entertainment for every event",
             "Get Started", "slider/2021/banner2.png"),
            ("Turn talent into livelihood", "A platform built for creators",
             "Join Now", "slider/2021/banner3.png"),
        ]
        created = 0
        for headerline, subtitle, button_text, photo in sliders:
            _, was_created = Slider.objects.get_or_create(
                headerline=headerline,
                defaults={
                    "subtitle": subtitle,
                    "button_text": button_text,
                    "photo": photo,
                    "link": "#",
                },
            )
            created += was_created
        self.stdout.write(f"  sliders: {created} created")

    def _create_team(self):
        members = [
            ("Aarav", "Sharma", "Founder & CEO", "team/2021/05/12/t1.png"),
            ("Diya", "Patel", "Head of Partnerships", "team/2021/05/12/t2.png"),
            ("Vivaan", "Singh", "Lead Engineer", "team/2021/05/12/t3.png"),
            ("Ananya", "Gupta", "Design Lead", "team/2021/05/12/t4.png"),
            ("Ishaan", "Kumar", "Community Manager", "team/2021/05/12/t5.png"),
        ]
        created = 0
        for first_name, last_name, role, photo in members:
            _, was_created = Team.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                defaults={
                    "role": role,
                    "photo": photo,
                    "fb_link": "#",
                    "insta_link": "#",
                    "youtube_link": "#",
                },
            )
            created += was_created
        self.stdout.write(f"  team: {created} created")

    def _create_youtubers(self):
        tubers = [
            ("CodeWithRhea", 15000, "Delhi", "code", "canon", "solo", "1.2M",
             "y1.png", True),
            ("TechDrift", 12000, "Mumbai", "mobile_review", "sony", "small", "850K",
             "y2.png", True),
            ("WanderVlogs", 9000, "Bengaluru", "vlog", "fuji", "small", "600K",
             "y3.png", False),
            ("LaughFactory", 20000, "Delhi", "comedy", "nikon", "large", "2.4M",
             "y4.png", True),
            ("GameZone", 18000, "Pune", "gaming", "red", "solo", "1.8M",
             "y5.png", False),
            ("KitchenTales", 8000, "Chennai", "cooking", "others", "solo", "450K",
             "y6.png", False),
        ]
        created = 0
        for (name, price, city, category, camera, crew, subs, img,
             featured) in tubers:
            _, was_created = Youtuber.objects.get_or_create(
                name=name,
                defaults={
                    "price": price,
                    "photo": f"ytubers/2021/05/{img}",
                    "video_url": "dQw4w9WgXcQ",
                    "description": (
                        f"<p>{name} is a talented creator specialising in "
                        f"{category.replace('_', ' ')} content.</p>"
                    ),
                    "city": city,
                    "age": 27,
                    "height": 175,
                    "crew": crew,
                    "camera_type": camera,
                    "subs_count": subs,
                    "category": category,
                    "is_featured": featured,
                },
            )
            created += was_created
        self.stdout.write(f"  youtubers: {created} created")
