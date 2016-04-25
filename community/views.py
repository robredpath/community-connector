from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from open_facebook import OpenFacebook
from community.models import UserProfile

import logging

logger = logging.getLogger(__name__)


def index(request):
    def group_name_id(group):
        return {
            'name': group['name'],
            'id': group['id'],
        }

    context = {}

    if request.user.is_authenticated():
        # Get the user's groups for display
        # TODO: implement paging
        fb = OpenFacebook(request.user.access_token, version="v2.6")
        fb_groups = list(map(group_name_id, fb.get("me/groups")["data"]))
        context.update({
            'fb_groups': fb_groups,
        })

        try:
            current_fb_group = list(filter(
                lambda group: group['id'] ==
                request.user.userprofile.facebook_group,
                fb_groups
            ))[0]
        except ObjectDoesNotExist:
            current_fb_group = "None"

        context.update({
                'current_fb_group': current_fb_group
            })

        if request.POST and request.POST['facebook_group']:
            user_profile, created = UserProfile.objects.get_or_create(
                    user=request.user.get_user()
                )
            user_profile.facebook_group = request.POST['facebook_group']
            user_profile.save()
            current_fb_group = list(filter(
                lambda group: group['id'] == request.POST['facebook_group'],
                fb_groups
            ))[0]
            context.update({
                'current_fb_group': current_fb_group
            })

    return render(request, 'community/index.html', context)
