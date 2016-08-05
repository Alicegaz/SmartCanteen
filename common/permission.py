from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate


def have_permission(request, permission=None):
    user = request.user
    if isinstance(user, AnonymousUser):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
        except Exception:
            return False
        user = authenticate(username=username, password=password)
        print(user)
    if user is not None:
        if permission is not None:
            for perm in permission:
                if user.has_perm(perm):
                    return user
            return False
        else:
            return user
    else:
        return False
