from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def validate_future(dt):
    if dt < timezone.now():
        raise ValidationError(
            _('%(date)s is not in the future'), params={'date': dt}
        )


class Message(models.Model):
    message_text_long = models.CharField(max_length=4000)
    message_text_short = models.CharField(max_length=160)
    sms_has_been_sent = models.BooleanField(
        default=False,
        editable=False
    )
    email_has_been_sent = models.BooleanField(
        default=False,
        editable=False
    )

    def __str__(self):
        return "Long message ({}): {} Short message ({}): {}".format(
            'Sent' if self.email_has_been_sent else 'Unsent',
            self.message_text_long,
            'Sent' if self.sms_has_been_sent else 'Unsent',
            self.message_text_short
         )


class Event(models.Model):
    # We store details of all the events that we know about
    start_time = models.DateTimeField(validators=[validate_future])
    end_time = models.DateTimeField(validators=[validate_future])
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=4000)
    # eg the Facebook event ID.
    # CharField because we're never doing maths with this value and other
    # providers might use non-numeric IDs
    external_id = models.CharField(max_length=128)
    # Saves a refactor if we ever support other event sources
    external_source = models.CharField(max_length=64, default="facebook")

    def __str__(self):
        return "{}: {} to {}".format(
            self.title,
            self.start_time,
            self.end_time
        )


class UserProfile(models.Model):
    # A profile for users, to store settings
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    # CharField because we're never doing maths with this value
    facebook_group = models.CharField(max_length=128)
    events = models.ManyToManyField(Event, blank=True)
