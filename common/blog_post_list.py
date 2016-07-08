from blog.models import Menu


def get_menu_of_current_time():
    menu_list = Menu.objects.all()
    if menu_list.__len__() == 0:
        return None
    else:
        result = menu_list[0]
        for menu in menu_list:
            if menu.date > result.date:
                result = menu
        return result
