from django.shortcuts import render

from open_facebook import OpenFacebook

import logging

logger = logging.getLogger(__name__)


def set_group_for_user(group_id):
    pass


def index(request):
    def group_name_id(group):
        return {
            'name': group['name'],
            'id': group['id'],
        }

    context = {}

    if request.user.is_authenticated:
        # Get the user's groups, and let them select one
        fb = OpenFacebook(request.user.access_token, version="v2.6")
        groups = list(map(group_name_id, fb.get("me/groups")["data"]))
        context = {
            'groups': groups,
        }

    return render(request, 'community/index.html', context)
