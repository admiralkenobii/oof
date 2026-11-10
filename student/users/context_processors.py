from .models import UserProfile

def user_profile(request):
    profile = None

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            pass

    return {"user_profile": profile}
