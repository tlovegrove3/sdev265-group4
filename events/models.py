from decimal import Decimal

from django.conf import settings
from django.db import models


class Category(models.Model):
    """
    Predefined event categories.

    Categories are managed by developers, not end users.
    Seeded via data migration (e.g., Social, Meeting, Workshop, Sports, Music).

    Examples:
        Category.objects.all()                    # All categories (for dropdowns)
        event.category.name                       # Get category name for display
        Category.objects.get(name="Workshop")     # Lookup by name
    """

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "events_category"
        verbose_name_plural = "categories"
        ordering = ["name"]  # Alphabetical in dropdowns

    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Core event model.

    Represents a user-created event with all details needed for display,
    filtering, and permission checks. Only the creator can edit/cancel.

    Key relationships:
        event.creator           -> User who created the event
        event.category          -> Category this event belongs to
        event.rsvps.all()       -> All RSVPs for this event
        event.rsvps.count()     -> Attendee count
        user.created_events.all() -> All events a user created

    Status flow:
        active -> cancelled     (creator cancels, event stays visible)
        active -> draft         (future: save without publishing)

    Query patterns:
        Event.objects.filter(status='active').order_by('date_time')
        Event.objects.filter(category__name='Workshop')
        Event.objects.filter(price__lte=Decimal('50.00'))
    """

    # --- Status choices ---
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        CANCELLED = "cancelled", "Cancelled"
        DRAFT = "draft", "Draft"  # Not in MVP, but free to define now

    # --- Fields ---

    # Event details
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=300)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Display-only price. 0.00 = free event.",
    )

    # Relationships
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  # Prevent deleting categories that have events
        related_name="events",
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # Delete user -> delete their events
        related_name="created_events",
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "events_event"
        ordering = ["date_time"]  # Default sort: soonest first

    def __str__(self):
        return self.title


class RSVP(models.Model):
    """
    Tracks user attendance for events.

    Simple existence-based model: row exists = user is attending.
    Cancelling an RSVP deletes the row.

    The unique_together constraint prevents duplicate RSVPs at the
    database level — same concept as a composite primary key on a
    junction table in SQL Server.

    Key query patterns:
        event.rsvps.count()                          # Attendee count
        event.rsvps.select_related('user').all()     # Attendee list
        RSVP.objects.filter(user=user, event=event)  # Check if user RSVPed
        user.rsvps.select_related('event').all()     # User's RSVPed events
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # Delete user -> delete their RSVPs
        related_name="rsvps",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,  # Delete event -> delete its RSVPs
        related_name="rsvps",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "events_rsvp"
        unique_together = ["user", "event"]  # One RSVP per user per event
        verbose_name = "RSVP"
        verbose_name_plural = "RSVPs"

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"
