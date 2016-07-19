from common.permission import have_permission
from django.core.exceptions import PermissionDenied


def user_have_permission(permission):
    def decorator(view_func):
        def func_decorator(request, *args, **kwargs):
            if have_permission(request, permission):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return func_decorator
    return decorator
