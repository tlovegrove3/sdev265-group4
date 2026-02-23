import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from events.models import Category, Event


class Command(BaseCommand):
    help = "Seed test users and sample events for development"

    def handle(self, *args, **options):
        # --- Test Users ---
        test_users = [
            ("testuser1", "testuser1@example.com", "TestPass123!"),
            ("testuser2", "testuser2@example.com", "TestPass123!"),
            ("testuser3", "testuser3@example.com", "TestPass123!"),
            ("testuser4", "testuser4@example.com", "TestPass123!"),
            ("testuser5", "testuser5@example.com", "TestPass123!"),
        ]

        users = []
        for username, email, password in test_users:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email},
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f"  Created user: {username}")
            else:
                self.stdout.write(f"  User exists: {username}")
            users.append(user)

        # --- Sample Events ---
        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write(self.style.ERROR("No categories found. Run migrate first."))
            return

        locations = [
            "Main Hall, Building A",
            "Community Center, Room 204",
            "City Park Pavilion",
            "Downtown Conference Center",
            "Virtual (Zoom)",
            "Student Union, Floor 2",
            "Public Library, Meeting Room B",
        ]

        sample_events = [
            (
                "Spring Coding Bootcamp",
                "Intensive weekend workshop covering Python fundamentals and web development basics.",
                0,
            ),
            (
                "Community Garden Cleanup",
                "Join us for a morning of gardening and community building. Tools provided.",
                0,
            ),
            ("Local Band Night", "Three local bands perform original music. Food trucks on site.", 15),
            ("Wedding Planning Workshop", "Expert tips on planning your perfect day on a budget.", 25),
            ("Charity 5K Run", "Annual charity run supporting local food banks. All ages welcome.", 30),
            ("Kids Art Camp", "Creative art activities for ages 5-12. Materials included.", 10),
            ("Tech Meetup: AI in 2026", "Panel discussion on practical AI applications in small business.", 0),
            ("Corporate Networking Mixer", "Connect with local business leaders over appetizers and drinks.", 20),
            ("Outdoor Yoga Session", "Sunrise yoga in the park. Bring your own mat.", 5),
            ("Seasonal Craft Fair", "Handmade goods from 30+ local artisans. Free admission.", 0),
            ("Private Dinner Party", "Intimate chef-prepared dinner for invited guests.", 75),
            ("Film Screening & Discussion", "Independent documentary screening followed by director Q&A.", 10),
            ("Food Truck Festival", "Twelve food trucks, live music, and lawn games.", 0),
            ("Resume Writing Workshop", "Get your resume reviewed by HR professionals.", 0),
            ("Basketball Tournament", "3-on-3 tournament. Register your team by March 1.", 15),
        ]

        base_date = timezone.make_aware(timezone.datetime(2026, 2, 25, 10, 0))

        events_created = 0
        for i, (title, description, price) in enumerate(sample_events):
            # Spread events across the date range
            event_date = base_date + timedelta(days=i * 2, hours=random.randint(0, 8))
            creator = users[i % len(users)]
            category = random.choice(categories)

            _, created = Event.objects.get_or_create(
                title=title,
                defaults={
                    "description": description,
                    "date_time": event_date,
                    "location": random.choice(locations),
                    "price": Decimal(str(price)),
                    "category": category,
                    "creator": creator,
                },
            )
            if created:
                events_created += 1

        self.stdout.write(self.style.SUCCESS(f"Done! {len(users)} users, {events_created} events seeded."))
