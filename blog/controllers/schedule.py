from common.permission import have_permission
from blog.models import Schedule


def delete_date(post_dict):
    try:
        post_dict.pop('date')
    except Exception:
        pass


def have_items(post_dict):
    try:
        post_dict.get('items')
    except Exception:
        return False
    return True

def schedule_edit(request, menu):
    menu = Schedule.objects.all().get(pk=1)
    user = have_permission(request)
    if user:
        obj_dict = menu.__dict__
        request_dict = request.POST
        delete_date(request_dict)
        for item in request_dict.items():
            key, value = item
            if key in obj_dict:
                if value:
                    obj_dict[key] = value
        menu.save()
        return menu
    return False


def create_schedule(request):
    user = have_permission(request)
    if user:
        menu = Schedule()
        menu.author = user
        menu.save()
        return schedule_edit(request, menu)
    return False
