from django.utils import timezone

from blog.controllers.dish import contain_ingredients, delete_all_ingredients, add_ing_dish_relations
from common.permission import have_permission
from common.request import get_image_from_request
from blog.models import Shares


# TODO need roles
def create_shares(request):
    user = have_permission(request)
    if user:
        share = Shares.objects.create(author=user)
        share_dict = share.__dict__
        request_dict = request.POST
        end_date = request.POST.get('end_date')
        start_date = request.POST.get('start_date')
        image = get_image_from_request(request)
        if 'image' in request.POST:
            del request.POST['image']
        for item in request_dict.items():
            key, value = item
            if key in share_dict:
                if value:
                    share_dict[key] = value
        try:
            if image:
                share.image = image
        except AttributeError:
            pass
        try:
            if end_date and start_date:
                share.end_date = end_date
                share.start_date = start_date
            else:
                share.end_date = timezone.now()
                share.start_date = timezone.now()
        except AttributeError:
            pass
        share.save()
        return share.id
    else:
        return False

        # TODO need roles


def shares_edit(request, share):
    user = have_permission(request)
    if user:
        obj_dict = share.__dict__
        request_dict = request.POST
        image = get_image_from_request(request)
        if 'image' in request.POST:
            del request.POST['image']
        for item in request_dict.items():
            key, value = item
            if key in obj_dict:
                if value:
                    obj_dict[key] = value
        try:
            if image:
                share.image = image
        except AttributeError:
            pass
        share.author = user
        share.save()
        return share.id
    else:
        return False