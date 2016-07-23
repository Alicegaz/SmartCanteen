from blog.forms import SharesForm, ContactsForm
from blog.models import Shares, Contacts
from blog.forms import PostForm, IngredientsForm, MenuForm, ScheduleForm
from blog.models import Post, Ingredient, Menu, Schedule, History, Offers
from django.shortcuts import get_object_or_404, HttpResponse
from django.contrib import auth
from common.json_warper import json, json_response
from common.blog_post_list import get_menu_of_current_time
from django.shortcuts import redirect, render
from blog.controllers.shares import create_shares, shares_edit as shares_change
from blog.controllers.dish import dish_edit as dish_change, create_dish, buy, buy_dish_list
from blog.controllers.contacts import contact_edit as contact_сhange, create_contact
from blog.controllers.menu import create_menu, add_to_history
from blog.controllers.ingredient import ingredient_change, create_ingredient
from django.contrib.auth.decorators import permission_required
from common.decorators import user_have_permission
import pytz
utc = pytz.UTC


def dishes_list(request):
    dishes = Post.objects.all().order_by('created_date').filter(status=True)
    data = {'posts': dishes}
    if json(request):
        return json_response(dishes)
    else:
        return render(request, 'blog_templates/dishes_list.html', data)


def dish_details(request, pk=None):
    dish = get_object_or_404(Post, pk=pk)
    ingredients = dish.get_ingredients()

    class IngAm:
        ingredient = None
        amount = None

        def get_json_object(self):
            dic = self.__dict__
            dic['ingredient'] = dic['ingredient'].get_json_object()
            return dic

    ing_list = []
    for ing in ingredients:
        new_one = IngAm()
        new_one.ingredient = ing
        new_one.amount = dish.get_amount(ing)
        ing_list.append(new_one)
    context = {
        "instance": dish,
        "ingredients": ing_list,
    }
    if json(request):
        return json_response(context)
    return render(request, 'blog_templates/post_detail.html', context)


@permission_required('blog.can_add', raise_exception=True)
def dish_edit(request, pk):
    context = {}
    dish = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        dish = dish_change(request, dish)
        if dish is not False:
            return redirect('dishes_list')
        else:
            return redirect('no_permission')
    else:
        context['form'] = PostForm(instance=dish)
        context['posts'] = Ingredient.objects.all()
    return render(request, "blog_templates/post_edit.html", context)


@permission_required('blog.can_add', raise_exception=True)
def new_dish(request):
    context = {'posts': Ingredient.objects.all()}
    if request.method == 'POST':
        dish = create_dish(request)
        if dish is not False:
            return redirect('dishes_list')
        else:
            return redirect('no_permission')
    else:
        context['form'] = PostForm()
    return render(request, 'blog_templates/post_new.html', context)


@permission_required('blog.can_add', raise_exception=True)
def dish_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.status = False
    post.save()
    return redirect('dishes_list')


def menu_out(request):
    menu = get_menu_of_current_time()
    shares = Shares.objects.all().filter(carousel=True)
    data = {'posts': menu, 'shares': shares}
    if json(request):
        data.pop('shares')
        return json_response(menu)
    else:
        return render(request, 'blog_templates/post_list.html', data)


@permission_required('blog.can_add', 'blog.can_edit_schedule', raise_exception=True)
def history_out(request):
    history = History.objects.all().order_by('-menu__date')
    return render(request, 'blog_templates/history.html', {'history': history})


@permission_required('blog.can_add', 'blog.can_edit_schedule', raise_exception=True)
def menu_detail(request, pk=None):
    menu = get_object_or_404(Menu, pk=pk)
    items = menu.items.all()
    context = {
        "instance": menu,
        "items": items,
    }
    return render(request, 'blog_templates/menu_detail.html', context)


@permission_required('blog.can_add', raise_exception=True)
def menu_edit(request, pk):
    return new_menu(request, pk)


@permission_required('blog.can_add', 'blog.can_edit_shedule', raise_exception=True)
def new_menu(request, pk=None):
    if request.method == 'POST':
        menu = create_menu(request)
        if menu is not False:
            status = add_to_history(menu)
            if status:
                return redirect('/')
            else:
                return render(request, 'blog_templates/not_enough_ingredient.html')
        #         TODO create page
        else:
            return redirect('no_permission')
    else:
        if pk is not None:
            form = MenuForm(instance=Menu.objects.get(id=pk))
        else:
            form = MenuForm()
    return render(request, 'blog_templates/new_menu.html', {'form': form})


@permission_required('blog.can_add', raise_exception=True)
def menu_remove(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    menu.delete()
    return redirect('menu_archive')


@permission_required('blog.can_add', raise_exception=True)
def menu_item_remove(request, **kwargs):
    pk = kwargs.get('pk', '')
    post = Menu.objects.get(pk=pk)
    if post.items.count() == 1:
        post.delete()
    else:
        ite = post.items.get(pk=kwargs.get('item_pk', ''))
        post.items.remove(ite)
    return redirect('blog.views.menu_archive')


@permission_required('blog.can_add', 'blog.can_edit_schedule', raise_exception=True)
def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'blog_templates/post_ingredientlist.html', {'posts': ingredients})


@user_have_permission('blog.can_add')
def ingredient_detail(request, pk=None):
    instance1 = get_object_or_404(Ingredient, pk=pk)
    context = {
        "title": instance1.name,
        "instance": instance1,
        "username": auth.get_user(request).is_superuser
    }
    return render(request, 'blog_templates/post_ingredientdetail.html', context)


@permission_required('blog.can_add', raise_exception=True)
def ingredient_edit(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == "POST":
        ingredient = ingredient_change(request, ingredient)
        if ingredient is not False:
            return redirect('post_ingredientlist')
        else:
            return redirect('no_permission')
    else:
        form = IngredientsForm(instance=ingredient)
    return render(request, 'blog_templates/post_ingredientedit.html', {'form': form})


@permission_required('blog.can_add', raise_exception=True)
def new_ingredient(request):
    if request.method == 'POST':
        ingredient = create_ingredient(request)
        if ingredient is not False:
            return redirect('post_ingredientlist')
        else:
            return redirect('no_permission')
    else:
        form = IngredientsForm()
    return render(request, 'blog_templates/post_ingredientedit.html', {'form': form})


@permission_required('blog.can_add', raise_exception=True)
def ingredient_remove(request, pk):
    post = get_object_or_404(Ingredient, pk=pk)
    post.delete()
    return redirect('blog.views.post_ingredientlist')


# TODO создать страницу
def no_permission(request):
    return render(request, 'blog_templates/no_permission.html')


# TODO оценить полезнсть этого метода
def mymodel(request, pk=None):
    instance = get_object_or_404(Post, pk=pk)
    ingredientss = instance.ingredients.all()
    context = {
        "title": instance.title,
        "instance": instance,
        "ingredientss": ingredientss,

    }
    return render(request, 'blog_templates/mymodal.html', context)


# TODO оценить полезнсть этого метода
# @user_passes_test(user.is_stuff, '/have_no_permission')
# def post_admin(request):
#     if request.user.is_superuser:
#
#         args = {}
#         args.update(csrf(request))
#         args['username'] = auth.get_user(request).is_superuser
#         return render(request, 'blog_templates/post_admin.html', args)
#     else:
#         return HttpResponse("У вас нет прав администратора")

@permission_required('blog.can_add', 'blog.can_edit_schedule', raise_exception=True)
def schedule_new(request):
        if request.method == 'POST':
            form = ScheduleForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect('/')
        else:
            form = ScheduleForm()
        return render(request, 'blog_templates/schedule_new.html', {'form': form})


@permission_required('blog.can_add', 'blog.can_edit_schedule', raise_exception=True)
def schedule_edit(request, pk):
    post = get_object_or_404(Schedule, pk=pk)
    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=post)
        if form.is_valid():
            form.save_object(request=request)
            return redirect('/')
    else:
        form = ScheduleForm(instance=post)
    return render(request, "blog_templates/schedule_edit.html", {'form': form})


def shares_list(request):
    shares = Shares.objects.all().order_by('created_date')
    data = {'shares': shares}
    try:
        shares_active = []
        for sh in Shares.objects.all():
            if sh.is_past_due():
                shares_active.append(sh)
        data = {'shares': shares, 'shares_active': shares_active}
    except Exception:
        pass
    if json(request):
        return json_response(shares)
    else:
        return render(request, 'blog_templates/shares_list.html', data)


@permission_required('blog.can_add', 'blog.can_edit_schedule', raise_exception=True)
def shares_new(request):
    context = {}
    if request.method == 'POST':
        share = create_shares(request)
        if share is not False:
            return redirect('shares')
        else:
            return redirect('no_permission')
    else:
        context['form'] = SharesForm()
    return render(request, 'blog_templates/shares_new.html', context)


@permission_required('blog.can_add', 'blog.can_edit_schedule', raise_exception=True)
def shares_edit(request, pk):
    context = {}
    share = get_object_or_404(Shares, pk=pk)
    if request.method == "POST":
        share = shares_change(request, share)
        if share is not False:
            return redirect('shares')
        else:
            return redirect('no_permission')
    else:
        context['form'] = SharesForm(instance=share)
    return render(request, "blog_templates/shares_edit.html", context)


def buy_dishes(request):
    status = buy(request)
    if status:
        price, calories = status
        return json_response({'price': price, 'calories': calories})
    else:
        return HttpResponse("Wrong request", status=400)


def send_offer(request):
    dish_list = request.POST.getlist('dishes')
    status = buy_dish_list(dish_list)
    if status:
        return HttpResponse("OK", status=200)
    else:
        return HttpResponse("There is no such dishes in menu", status=400)


@permission_required('blog.can_add', raise_exception=True)
def get_offers(request):
    offers = Offers.objects.all()

    class OfferPrice:
        offer = None
        price = None
    result = []
    for offer in offers:
        price = 0
        dishes = offer.get_dish_list()
        for dish in dishes:
            price += dish.price * dish.amount
        obj = OfferPrice()
        obj.offer = offer
        obj.price = price
        result.append(obj)
    return render(request, "blog_templates/offers.html", {'offers': result})


@permission_required('blog.can_add', raise_exception=True)
def offer_detail(request, pk=None):
    offer = Offers.objects.get(id=pk)
    dish_list = offer.get_dish_list()
    price = 0
    for dish in dish_list:
        price += dish.price*dish.amount
    context = {
        'offer': offer,
        'dishes': dish_list,
        'price': price,
    }
    return render(request, "blog_templates/offer_detail.html", context)


def shares_detail(request, pk=None):
    share = get_object_or_404(Shares, pk=pk)
    active=share.is_past_due()
    context = {
        "instance": share,
        "active": active,
    }
    if json(request):
        return json_response(context)
    return render(request, 'blog_templates/shares_detail.html', context)


def contacts(request):
    contacts = Contacts.objects.all()
    return render(request, 'blog_templates/contacts.html', {'contacts': contacts})


@permission_required('blog.can_add', raise_exception=True)
def new_contact(request):
    context = {'posts': Contacts.objects.all()}
    if request.method == 'POST':
        contact = create_contact(request)
        if contact is not False:
            return redirect('contacts')
        else:
            return redirect('no_permission')
    else:
        context['form'] = ContactsForm()
    return render(request, 'blog_templates/contacts_form.html', context)


@permission_required('blog.can_add', raise_exception=True)
def contact_edit(request, pk):
    context = {}
    contact = get_object_or_404(Contacts, pk=pk)
    if request.method == "POST":
        contact = contact_сhange(request, contact)
        if contact is not False:
            return redirect('contacts')
        else:
            return redirect('no_permission')
    else:
        context['form'] = ContactsForm(instance=contact)
        context['posts'] = Contacts.objects.all()
    return render(request, "blog_templates/contact_edit.html", context)
