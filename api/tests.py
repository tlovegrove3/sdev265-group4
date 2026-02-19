from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from events.models import Event, Category, RSVP

User = get_user_model()

class EventAPITests(APITestCase):

    def setUp(self):
        # create two users and a category/event
        self.user = User.objects.create_user(username="alice", password="pass")
        self.other = User.objects.create_user(username="bob", password="pass")
        self.category = Category.objects.create(name="TestCat")
        self.event = Event.objects.create(
            title="Party",
            description="fun",
            date_time=timezone.now(),
            location="here",
            price=0,
            category=self.category,
            creator=self.user,
        )
        self.list_url = reverse("event-list")
        self.detail_url = reverse("event-detail", args=[self.event.pk])

    def test_anonymous_can_list_events(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.json()), 1)

    def test_anonymous_cannot_create_event(self):
        # anonymous should be blocked (403 with session auth)
        resp = self.client.post(self.list_url, {
            "title": "X",
            "description": "Y",
            "date_time": timezone.now(),
            "location": "Z",
            "price": 10,
            "category": self.category.pk,
            "creator": self.user.pk,
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_can_create_event(self):
        # log in using client helper
        self.client.force_authenticate(user=self.user) # type: ignore
        resp = self.client.post(self.list_url, {
            "title": "New",
            "description": "More",
            "date_time": timezone.now(),
            "location": "There",
            "price": 5,
            "category": self.category.pk,
            "creator": self.user.pk,
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.filter(title="New").count(), 1)

    def test_creator_can_update_event(self):
        # creator must be able to edit
        self.client.force_authenticate(user=self.user) # type: ignore
        resp = self.client.put(self.detail_url, {
            "title": "Party!,",
            "description": "fun",
            "date_time": timezone.now(),
            "location": "here",
            "price": 0,
            "category": self.category.pk,
            "creator": self.user.pk,
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "Party!,")

    def test_non_creator_cannot_update_event(self):
        # non-owner should still be forbidden
        self.client.force_authenticate(user=self.other) # type: ignore
        resp = self.client.patch(self.detail_url, {"title": "Hacked"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class RSVPACTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass")
        self.category = Category.objects.create(name="TestCat")
        self.event = Event.objects.create(
            title="Party",
            description="fun",
            date_time=timezone.now(),
            location="here",
            price=0,
            category=self.category,
            creator=self.user,
        )
        self.rsvp_list = reverse("rsvp-list")

    def test_anonymous_cannot_rsvp(self):
        # anonymous cannot RSVP (403 due to session auth)
        resp = self.client.post(self.rsvp_list, {
            "event": self.event.pk,
            "user": self.user.pk,
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_can_rsvp(self):
        # authenticate and then create RSVP
        self.client.force_authenticate(user=self.user) # type: ignore
        resp = self.client.post(self.rsvp_list, {
            "event": self.event.pk,
            "user": self.user.pk,
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RSVP.objects.filter(event=self.event, user=self.user).count(), 1)

