from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta
import pytz

from .models import Message, Event


class SignalsTests(TestCase):

    def test_creates_message_on_new_event_creation(self):
        """
        When a new Event is created, a new Message should be created as well
        """
        event = Event(
            start_time=timezone.now(),
            end_time=timezone.now(),
            title="Test Event"
        )
        event.save()
        self.assertEqual(Message.objects.count(), 1)


class EventsModelTests(TestCase):

    def test_events_start_in_the_future(self):
        """
        When a new Event is created, its start date should be in the future
        """

        event = Event(
            start_time=datetime.now(pytz.utc) - timedelta(days=10),
            end_time=datetime.now(pytz.utc) + timedelta(days=10),
            title="Test Event"
        )
        with self.assertRaisesMessage(ValidationError, 'is not in the future'):
            event.full_clean()

    def test_events_end_in_the_future(self):
        """
        When a new Event is created, its end date should be in the future
        """

        event = Event(
            start_time=datetime.now(pytz.utc) + timedelta(days=10),
            end_time=datetime.now(pytz.utc) - timedelta(days=10),
            title="Test Event"
        )
        with self.assertRaisesMessage(ValidationError, 'is not in the future'):
            event.full_clean()

    def test_events_end_after_they_start(self):
        """
        When a new Event is created, we should make sure that its end time is
        after its start time
        """
        event = Event(
            start_time=datetime.now(pytz.utc) + timedelta(days=10),
            end_time=datetime.now(pytz.utc) + timedelta(days=5),
            title="Test Event"
        )
        with self.assertRaisesMessage(ValidationError, 'is not in the future'):
            event.full_clean()
