from common.permission import have_permission
from common.blog_post_list import get_menu_of_current_time
from blog.models import Menu, Post
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


def have_items(post_dict):
    try:
        post_dict.get('items')
    except Exception:
        return False
    return True


def add_dishes_to_menu(post_dict, menu):
    items_list = post_dict.getlist('items')
    items_list = [Post.objects.get(id=item) for item in items_list]
    menu.items = items_list


# TODO need roles
def menu_edit(request, menu):
    user = have_permission(request)
    if user:
        obj_dict = menu.__dict__
        request_dict = request.POST
        if request_has_date(request.POST):
            time = add_date(request.POST, menu)
            delete_menus_of_current_time(time, request_dict.get('title'))
        if have_items(request_dict):
            add_dishes_to_menu(request_dict, menu)
        for item in request_dict.items():
            key, value = item
            if key in obj_dict:
                if value:
                    obj_dict[key] = value
        menu.save()
        return menu.id
    return False


def create_menu(request):
    user = have_permission(request)
    if user:
        request_dict = request.POST
        menu = Menu(title=request_dict.pop())
        menu.save()
        return menu_edit(request, menu)
    return False