from common.permission import have_permission
from common.blog_post_list import get_menu_of_current_time
import datetime


def request_has_date(post_dict):
    try:
        year = post_dict.get('date_year')
        month = post_dict.get('date_month')
        day = post_dict.get('date_day')
    except Exception:
        return False
    return True


def add_date(post_dict, menu):
    year = post_dict['date_year']
    month = post_dict['date_month']
    day = post_dict['date_day']
    time = datetime.date(
        year=int(year),
        month=int(month),
        day=int(day),
    )
    menu.date = time
    del post_dict['date_year']
    del post_dict['date_month']
    del post_dict['date_day']
    return time


def delete_menus_of_current_time(time, title):
    menu = get_menu_of_current_time(title=title, time=time)
    try:
        menu.delete()
    except AttributeError:
        pass


# TODO need roles
def menu_edit(request, menu):
    user = have_permission(request)
    if user:
        obj_dict = menu.__dict__
        request_dict = request.POST
        if request_has_date(request.POST):
            time = add_date(request.POST, menu)
            delete_menus_of_current_time(time, request_dict.get('title'))
        for item in request_dict.items():
            key, value = item
            if key in obj_dict:
                if value:
                    obj_dict[key] = value
        menu.save()
        return menu.id
    return False