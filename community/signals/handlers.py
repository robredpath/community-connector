from django.db.models.signals import pre_save
from django.dispatch import receiver
from community.models import Message, Event

import logging
logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Event)
def create_messages_for_event(sender, instance, **kwargs):
    logger.warn(instance)
    message = Message(
        message_text_long="New event: {0}".format(instance),
        message_text_short="New event: {0}".format(instance)
    )
    message.save()
