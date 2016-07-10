from common.permission import have_permission
from common.request import get_image_from_request
from blog.models import IngDishRelation
from blog.models import Ingredient
from blog.models import Post


def delete_all_ingredients(dish):
    for ing_r in IngDishRelation.objects.filter(dish=dish):
        ing_r.delete()


def add_ing_dish_relations(request, dish):
    print(IngDishRelation.objects.filter(dish=dish))
    quantity_list = request.getlist('quantity')
    ingredients = request.getlist('ingredients')
    for (item, quantity) in zip(ingredients, quantity_list):
        item = Ingredient.objects.get(id=item)
        ing_r = IngDishRelation.objects.create(dish=dish, ingredient=item, amount=quantity)
        ing_r.save()


def contain_ingredients(request):
    try:
        quantity_list = request.getlist('quantity')
        ingredients = request.getlist('ingredients')
    except Exception:
        return False
    return True


# TODO need roles
def dish_edit(request, dish):
    user = have_permission(request)
    if user:
        obj_dict = dish.__dict__
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
                dish.image = image
        except AttributeError:
            pass
        dish.author = user
        dish.save()
        if contain_ingredients(request.POST):
            delete_all_ingredients(dish)
            add_ing_dish_relations(request.POST, dish)
        return dish.id
    else:
        return False


# TODO need roles
def create_dish(request):
    user = have_permission(request)
    if user:
        dish = Post.objects.create(author=user)
        dish_dict = dish.__dict__
        request_dict = request.POST
        image = get_image_from_request(request)
        if 'image' in request.POST:
            del request.POST['image']
        for item in request_dict.items():
            key, value = item
            if key in dish_dict:
                if value:
                    dish_dict[key] = value
        try:
            if image:
                dish.image = image
        except AttributeError:
            pass
        dish.save()
        if contain_ingredients(request.POST):
            add_ing_dish_relations(request.POST, dish)
        return dish.id
    else:
        return False
