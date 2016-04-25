from django.core.management.base import BaseCommand

from django_facebook.models import FacebookCustomUser
from open_facebook import OpenFacebook

from community.models import Event

import time
from datetime import timedelta
import dateutil.parser

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Compares the current state of Facebook to the current \
     state of our database. In the process of making updates, sends \
     notifications, updates calendars etc as necessary'

    def handle(self, *args, **options):

        for user in FacebookCustomUser.objects.all():
            fb = OpenFacebook(user.access_token, version="v2.6")
            group_events = fb.get(
                "{0}/events".format(user.userprofile.facebook_group),
                since=int(time.time())
                )

            if len(group_events['data']) > 0:
                for group_event in group_events['data']:
                    if 'end_time' in group_event:
                        end_time = group_event['end_time']
                    else:
                        end_time = (dateutil.parser.parse(
                                group_event['start_time']
                            ) + timedelta(hours=3))

                    event, created = Event.objects.get_or_create(
                        external_id=group_event['id'],
                        start_time=group_event['start_time'],
                        end_time=str(end_time),
                        title=group_event['name'],
                    )

                if event not in list(user.userprofile.events.all()):
                    user.userprofile.events.add(event)
                    user.save()

            # TODO: Handle changes in event times
