from django.core.management.base import BaseCommand
from community.models import Message
from django.contrib.auth.models import User
from django.conf import settings

# Intended to be run as a cron


class Command(BaseCommand):
    help = 'Runs the message queue, attempting to send any messages that \
     have not yet been sent'

    def handle(self, *args, **options):
        for message in Message.objects.filter(email_has_been_sent=False):
            for user in User.objects.all():
                subject = "New messages from %s" % settings.COMMUNITY_NAME
                user.email_user(subject, message.message_text_long)
                message.email_has_been_sent = True
                message.save()
                self.stdout.write(self.style.SUCCESS(
                    'Successfully sent email to "%s"' % user
                    )
                )
            # TODO: Implement SMS messaging as well
