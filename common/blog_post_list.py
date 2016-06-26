from django.utils import timezone
from blog.models import Menu


def __get_title_of_current_time():
    hour = timezone.now().hour
    if 11 <= hour <= 16:
        return 'обед'
    elif 16 <= hour <= 20:
        return 'ужин'
    else:
        return 'завтрак'


def get_menu_of_currunt_time():
    return Menu.objects.all().filter(date__month=timezone.now().month, date__day=timezone.now().day,
                                      date__year=timezone.now().year, title=__get_title_of_current_time())
