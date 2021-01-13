"""
Utility functions to be used by entire site
"""
from profiles.models import UserProfile


def get_profile_or_none(request):
    """ Function returns a valid UserProfile or None """
    try:
        return UserProfile.objects.get(user=request.user)
    except:
        return None