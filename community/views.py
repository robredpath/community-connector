from django.shortcuts import render

from open_facebook import OpenFacebook
from django_facebook.models import FacebookCustomUser
from community.models import GroupProfile

import logging, pickle

logger = logging.getLogger(__name__)


def index(request):
    def group_name_id(group):
        return {
            'name': group['name'],
            'id': group['id'],
        }

    context = {}

    if request.user.is_authenticated:
        rob = FacebookCustomUser.objects.get()
        logger.warn(rob == request.user)
        logger.warn(request.user.groupprofile.group)

        # Get the user's groups for display
        # TODO: implement paging
        fb = OpenFacebook(request.user.access_token, version="v2.6")
        groups = list(map(group_name_id, fb.get("me/groups")["data"]))
        context.update({
            'groups': groups,
        })

        current_group = list(filter(
                lambda group: group['id'] ==
                    str(request.user.groupprofile.group),
                groups
            ))[0]

        context.update({
                'current_group': current_group
            })

        if request.POST and request.POST['group']:
            group_profile, created = GroupProfile.objects.get_or_create(
                    user=request.user.get_user()
                )
            group_profile.group=request.POST['group']
            group_profile.save()
            current_group = list(filter(
                lambda group: group['id'] ==
                    str(request.POST['group']),
                groups
            ))[0]
            context.update({
                'current_group': current_group
            })


    return render(request, 'community/index.html', context)
