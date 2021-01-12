from profiles.models import UserProfile
from PIL import Image

"""
Utility functions to be used by entire site
"""

def get_profile_or_none(request):
    """ Function returns a valid UserProfile or None """
    try:
        return UserProfile.objects.get(user=request.user)
    except:
        return None

def size_profile_image(input_image):
    print('im in!')
    im = Image.open(input_image)
    if im.height < 400:
        print(">")
    else: 
        print("<")


size_profile_image('media/profile_images/instructor_2.jpg')