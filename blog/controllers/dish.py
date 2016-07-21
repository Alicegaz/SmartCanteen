from common.permission import have_permission
from common.request import get_image_from_request
from common.blog_post_list import get_menu_of_current_time
from blog.models import IngDishRelation, Ingredient, Post, Offers, DishAmount



def delete_all_ingredients(dish):
    for ing_r in IngDishRelation.objects.filter(dish=dish):
        ing_r.delete()


def add_ing_dish_relations(request, dish):
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


def get_dishes_list(request):
    id_list = request.getlist('dish_id')
    result = [Post.objects.get(id) for id in id_list]
    return result


def is_in_menu(dish_list):
    menu = get_menu_of_current_time()
    for item in dish_list:
        if item in menu.items.all():
            return False
    return True


def add_to_history(offer):
    offer.status = True
    offer.save()


def dishes_price(dish_list):
    result = 0
    for dish in dish_list:
        if dish.price:
            result += dish.price
    return result


def get_calories(dish_list):
    result = 0
    for dish in dish_list:
        if dish.calories:
            result += dish.calories
    return result


def contain_offer(request):
    try:
        s = request.POST.get('offer')
        if s is None:
            return False
        else:
            return True
    except:
        return False


def contain_dishes(request):
    try:
        s = request.POST.get('item')
        if s is None:
            return False
        else:
            return True
    except:
        return False


def buy_dish_list(dish_list):
    if is_in_menu(dish_list):
        offer = Offers(menu=get_menu_of_current_time())
        offer.save()
        for dish in dish_list:
            dish = Post.objects.get(id=dish)
            try:
                dish_amount = DishAmount.objects.get(offer=offer,dish = dish)
            except:
                dish_amount = None
            if dish_amount is None:
                dish_amount = DishAmount.objects.create(offer=offer, dish=dish)
            else:
                dish_amount.amount += 1
            dish_amount.save()
        offer.save()
        return True
    else:
        return False


def buy(request):
    if contain_offer(request):
        offer = request.POST.get('offer')
        offer = Offers.objects.get(id=offer)
        add_to_history(offer)
        return dishes_price(offer.items.all()), get_calories(offer.items.all())
    elif contain_dishes(request):
        dish_list = request.POST.getlist('item')
        buy_dish_list(dish_list)
        dish_list = [Post.objects.get(id=i) for i in dish_list ]
        return dishes_price(dish_list), get_calories(dish_list)
    else:
        return False
