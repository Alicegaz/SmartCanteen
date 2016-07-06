from common.permission import have_permission
from blog.models import Ingredient


def ingredient_change(request, ingredient):
    user = have_permission(request)
    if user:
        obj_dict = ingredient.__dict__
        request_dict = request.POST
        for item in request_dict.items():
            key, value = item
            if key in obj_dict:
                if value:
                    obj_dict[key] = value
        ingredient.save()
        return ingredient.id
    return False


def create_ingredient(request):
    user = have_permission(request)
    if user:
        request_dict = request.POST
        ingredient = Ingredient(name=request.POST)
        return ingredient_change(request, ingredient)
    return False