from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate


def have_permission(request, permmission=None):
    user = request.user
    if isinstance(user, AnonymousUser):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
        except Exception:
            return False
        user = authenticate(username=username, password=password)
    if permmission is not None and user is not None:
        if user.has_perm(permmission):
            return user
    else:
        return user
