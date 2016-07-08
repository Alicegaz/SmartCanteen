from blog.forms import PostForm, IngredientsForm, MenuForm, ScheduleForm
from blog.models import Post, Ingredient, Menu, Schedule
from django.shortcuts import get_object_or_404
from django.contrib import auth
from common.json_warper import json, json_response
from common.blog_post_list import get_menu_of_current_time
from django.shortcuts import redirect, render
from blog.controllers.dish import dish_edit as dish_change, create_dish
from blog.controllers.menu import menu_edit as change_menu, create_menu
from blog.controllers.ingredient import ingredient_change, create_ingredient


def dishes_list(request):
    dishes = Post.objects.all().order_by('created_date')
    data = {'posts': dishes}
    if json(request):
        return json_response(dishes)
    else:
        return render(request, 'blog_templates/dishes_list.html', data)


def dish_details(request, pk=None):
    dish = get_object_or_404(Post, pk=pk)
    ingredients = dish.get_ingredients()
    context = {
        "instance": dish,
        "ingredients": ingredients,
    }
    if json(request):
        return json_response(context)
    return render(request, 'blog_templates/post_detail.html', context)


# TODO need roles
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


# TODO need roles
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


# TODO запретить удалять не админам
def dish_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog.views.dishes_list')


def menu_out(request):
    menu = get_menu_of_current_time()
    data = {'posts': menu}
    if json(request):
        return json_response(menu)
    else:
        return render(request, 'blog_templates/post_list.html', data)


# TODO запретить видеть не админам
def menu_list(request):
    menu = Menu.objects.all()
    return render(request, 'blog_templates/menu_archive.html', {'posts': menu})


# TODO запретить видеть не админам
def menu_detail(request, pk=None):
    menu = get_object_or_404(Menu, pk=pk)
    items = menu.items.all()
    context = {
        "instance": menu,
        "items": items,
    }
    return render(request, 'blog_templates/menu_detail.html', context)


# TODO need roles
def menu_edit(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        menu = change_menu(request, menu)
        if menu is not False:
            return redirect('menu_detail', pk=menu)
        else:
            return redirect('no_permission')
    else:
        form = MenuForm(instance=menu)
    return render(request, "blog_templates/menu_edit.html", {'form': form})


# TODO need roles
def new_menu(request):
    if request.method == 'POST':
        menu_id = create_menu(request)
        if menu_id is not False:
            return redirect('/')
        else:
            return redirect('no_permission')
    else:
        form = MenuForm()
    return render(request, 'blog_templates/new_menu.html', {'form': form})


# TODO запретить удалять не админам
def menu_remove(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    menu.delete()
    return redirect('menu_archive')


# TODO запретить удалять не админам
def menu_item_remove(request, **kwargs):
    pk = kwargs.get('pk', '')
    post = Menu.objects.get(pk=pk)
    if post.items.count() == 1:
        post.delete()
    else:
        ite = post.items.get(pk=kwargs.get('item_pk', ''))
        post.items.remove(ite)
    return redirect('blog.views.menu_archive')


# TODO запретить видеть не админам
def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'blog_templates/post_ingredientlist.html', {'posts': ingredients})


# TODO запретить видеть не админам
def ingredient_detail(request, pk=None):
    instance1 = get_object_or_404(Ingredient, pk=pk)
    context = {
        "title": instance1.name,
        "instance": instance1,
        "username": auth.get_user(request).is_superuser
    }
    return render(request, 'blog_templates/post_ingredientdetail.html', context)


# TODO need roles
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


# TODO need roles
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


# TODO запретить удалять не админам
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


def schedule_edit(request, pk):
    post = get_object_or_404(Schedule, pk=pk)
    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save_object(request=request)
            return redirect('/')
    else:
        form = ScheduleForm(instance=post)
    return render(request, "blog_templates/schedule_edit.html", {'form': form})
