from django.utils import timezone
from blog.models import Menu


def __get_title_of_current_time(time):
    hour = time.hour
    if 11 <= hour <= 16:
        return 'обед'
    elif 16 <= hour <= 22:
        return 'ужин'
    else:
        return 'завтрак'


def get_menu_of_current_time(time=timezone.now(), title=None):
    if not title:
        title = __get_title_of_current_time(time)
    return Menu.objects.all().filter(date__month=time.month, date__day=time.day, date__year=time.year, title=title)
