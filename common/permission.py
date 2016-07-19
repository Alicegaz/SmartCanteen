from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate


def have_permission(request, role=None):
    user = request.user
    if isinstance(user, AnonymousUser):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
        except Exception:
            return False
        user = authenticate(username=username, password=password)
        print(user)
    if role is not None:
        if user.user_permissions.contain(role):
            return user
    else:
        return user
