from django.utils import timezone

from blog.controllers.dish import contain_ingredients, delete_all_ingredients, add_ing_dish_relations
from common.permission import have_permission
from common.request import get_image_from_request
from blog.models import Shares, Contacts


def create_contact(request):
    user = have_permission(request)
    if user:
        contact = Contacts.objects.create(author=user)
        contact_dict = contact.__dict__
        request_dict = request.POST
        image = get_image_from_request(request)
        if 'image' in request.POST:
            del request.POST['image']
        for item in request_dict.items():
            key, value = item
            if key in contact_dict:
                if value:
                    contact_dict[key] = value
        try:
            if image:
                contact.image = image
        except AttributeError:
            pass
        contact.save()
        return contact.id
    else:
        return False


def contact_edit(request, contact):
    user = have_permission(request)
    if user:
        obj_dict = contact.__dict__
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
                contact.image = image
        except AttributeError:
            pass
        contact.author = user
        contact.save()
        return contact.id
    else:
        return False