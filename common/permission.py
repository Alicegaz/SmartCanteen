from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate


def have_permission(request, role=None):
    user = request.user
    if user is AnonymousUser:
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
        except:
            return False
        user = authenticate(username, password)
    if role is not None:
        if user.user_permissions.contain(role):
            return user
    else:
        return user
