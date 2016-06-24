from .models import Menu
# from .forms import PostForm, IngredientsForm, MenuForm
from datetime import timedelta

from blog.forms import PostForm, IngredientsForm, MenuForm
from blog.models import Post, Ingredient, Menu
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
# from .forms import PostForm, IngredientsForm, MenuForm
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.template.context_processors import csrf
from common.views import json, json_response
from django.core import serializers
from django.shortcuts import render_to_response, redirect, render


def post_list(request):
    json = request.GET.get('json')
    start_date = timezone.now()
    end_date = start_date + timedelta(days=1)
    end_date1 = end_date + timedelta(days=1)
    # DATE_FORMAT = '%Y-%m-%d'
    # start_date = datetime.strptime(start_date, DATE_FORMAT)
    # qs = qs.filter(
    #   start_date__year=start_date.year,
    #  start_date__month=start_date.month,
    # start_date__day=start_date.day
    # )
    # compare current date without time with one in the database
    # now_time = datetime.now()
    # start = DateTime.Parse("2016-03-26T07:00:15+02").ToUniversalTime().time;
    # end = DateTime.Parse("2016-03-27T10:00:15+03").ToUniversalTime().time;
    # start2= DateTime.Parse("2016-03-26T11:00:15+02").ToUniversalTime().time;
    # end2 = DateTime.Parse("2016-03-27T15:00:15+03").ToUniversalTime().time;
    # start3 = DateTime.Parse("2016-03-26T16:00:15+02").ToUniversalTime().time;
    # end3 = DateTime.Parse("2016-03-27T20:00:15+03").ToUniversalTime().time;
    if 7 <= timezone.now().hour <= 11:
        posts = Menu.objects.all().filter(date__month=timezone.now().month, date__day=timezone.now().day,
                                          date__year=timezone.now().year, title='завтрак')
        if not json:
            return render(request, 'blog/post_list.html', {'posts': posts})

        else:
            data = {'posts': serializers.serialize('json', posts)}
            return JsonResponse(data)
    elif 11 <= timezone.now().hour <= 16:
        posts = Menu.objects.all().filter(date__month=timezone.now().month, date__day=timezone.now().day,
                                          date__year=timezone.now().year, title='обед')
        if not json:
            return render(request, 'blog/post_list.html', {'posts': posts})

        else:
            data = {'posts': serializers.serialize('json', posts)}
            return JsonResponse(data)
    elif 16 <= timezone.now().hour <= 20:
        posts = Menu.objects.all().filter(date__month=timezone.now().month, date__day=timezone.now().day,
                                          date__year=timezone.now().year, title='ужин')
        if not json:
            return render(request, 'blog/post_list.html', {'posts': posts})
        else:
            data = {'posts': serializers.serialize('json', posts)}
            return JsonResponse(data)
    else:
        posts = Menu.objects.all().filter(date__month=timezone.now().month, date__day=timezone.now().day,
                                          date__year=timezone.now().year, title='завтрак')
        if not json:
            return render(request, 'blog/post_list.html', {'posts': posts})

        else:
            data = {'posts': serializers.serialize('json', posts)}
            return JsonResponse(data)


def no_permission(request):
    return render(request, 'blog/no_permission.html')


def dishes_list(request):
    json = request.GET.get('json')
    posts = Post.objects.all().order_by('published_date')
    if not json:
        posts = Post.objects.all().order_by('published_date')
        return render(request, 'blog/dishes_list.html', {'posts': posts})
    else:
        data = {'posts': serializers.serialize('json', posts)}
        return JsonResponse(data)


def post_detail(request, pk=None):
    instance = get_object_or_404(Post, pk=pk)
    ingredientss = instance.ingredients.all()
    context = {
        "title": instance.title,
        "instance": instance,
        "ingredientss": ingredientss,

    }
    return render(request, 'blog/post_detail.html', context)


def mymodal(request, pk=None):
    instance = get_object_or_404(Post, pk=pk)
    ingredientss = instance.ingredients.all()
    context = {
        "title": instance.title,
        "instance": instance,
        "ingredientss": ingredientss,

    }
    return render(request, 'blog/mymodal.html', context)


# @user_passes_test(user.is_stuff, '/have_no_permission')
def post_admin(request):
    if request.user.is_superuser:

        args = {}
        args.update(csrf(request))
        args['username'] = auth.get_user(request).is_superuser
        return render(request, 'blog/post_admin.html', args)
    else:
        return HttpResponse("У вас нет прав администратора")


    # def post_ingredientlist(request):
    #    ingredientss = Ingredient.objects.all()
    #   return render(request, 'blog/post_ingredientlist', {'ingredientss': ingredientss})


def post_ingredientlist(request):
    posts = Ingredient.objects.all()
    return render(request, 'blog/post_ingredientlist.html', {'posts': posts})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()

            post_numder = post.pk
            for ing in request.POST.getlist('ingredients'):
                theing = Ingredient.objects.get(pk=ing)
                post.ingredients.add(theing.id)
            post.save()
            form.save_m2m()
            # messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
            # return HttpResponseRedirect(instance.get_absolute_url())
            context = {
                "title": post.title,
                "instance": post,
                "form": form,
            }
            # return render(request, 'blog/post_edit.html', context)
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {'form': form})


def menu_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = MenuForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()

            post_numder = post.pk
            for ing in request.POST.getlist('items'):
                theing = Post.objects.get(pk=ing)
                post.items.add(theing.id)
            post.save()
            form.save_m2m()
            # messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
            # return HttpResponseRedirect(instance.get_absolute_url())

            context = {
                "title": post.title,
                "instance": post,
                "form": form,
            }
            # return render(request, 'blog/post_edit.html', context)
            return redirect('menu_detail', pk=post.pk)

    else:
        form = PostForm(instance=post)
    return render(request, "blog/menu_edit.html", {'form': form})


def menu_detail(request, pk=None):
    instance = get_object_or_404(Menu, pk=pk)
    items = instance.items.all()
    context = {
        "title": instance.title,
        "instance": instance,
        "items": items,

    }
    return render(request, 'blog/menu_detail.html', context)

def breakfast_edit(request, pk):
    post = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = MenuForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.title = 'завтрак'
            post_numder = post.pk
            for ing in request.POST.getlist('items'):
                theing = Menu.objects.get(pk=ing)
                post.items.add(theing.id)

            post.save()
            form.save_m2m()
            # messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
            # return HttpResponseRedirect(instance.get_absolute_url())

            context = {
                "title": post.title,
                "instance": post,
                "form": form,
            }
            # return render(request, 'blog/post_edit.html', context)
            return redirect('/')

    else:
        form = MenuForm(instance=post)
    return render(request, "blog/breakfast_edit.html", {'form': form})


def supper_edit(request, pk):
    post = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = MenuForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.title = 'ужин'
            post_numder = post.pk
            for ing in request.POST.getlist('items'):
                theing = Menu.objects.get(pk=ing)
                post.items.add(theing.id)
            post.save()
            form.save_m2m()
            # messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
            # return HttpResponseRedirect(instance.get_absolute_url())

            context = {
                "title": post.title,
                "instance": post,
                "form": form,
            }
            # return render(request, 'blog/post_edit.html', context)
            return redirect('/')

    else:
        form = MenuForm(instance=post)
    return render(request, "blog/supper_edit.html", {'form': form})


def dinner_edit(request, pk):
    post = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = MenuForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.title = 'обед'
            post_numder = post.pk
            for ing in request.POST.getlist('items'):
                theing = Menu.objects.get(pk=ing)
                post.items.add(theing.id)
            post.save()
            form.save_m2m()
            # messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
            # return HttpResponseRedirect(instance.get_absolute_url())

            context = {
                "title": post.title,
                "instance": post,
                "form": form,
            }
            # return render(request, 'blog/post_edit.html', context)
            return redirect('/')

    else:
        form = MenuForm(instance=post)
    return render(request, "blog/dinner_edit.html", {'form': form})


def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            # post.ingredients()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def new_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST or None, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.date = timezone.now()
            post.save()
            form.save_m2m()
            # post.ingredients()
            return redirect('post_list')
    else:
        form = MenuForm()
    return render(request, 'blog/new_menu.html', {'form': form})


def post_ingredientdetail(request, pk=None):
    instance1 = get_object_or_404(Ingredient, pk=pk)
    context = {
        "title": instance1.name,
        "instance": instance1,
        "username": auth.get_user(request).is_superuser
    }
    return render(request, 'blog/post_ingredientdetail.html', context)


def post_ingredientedit(request, pk):
    post = get_object_or_404(Ingredient, pk=pk)
    if request.method == "POST":
        form = IngredientsForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            # post_numder = post.pk
            # messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
            # return HttpResponseRedirect(instance.get_absolute_url())
            context = {
                "title": post.name,
                "instance": post,
                "form": form,
            }
            return redirect('post_ingredientdetail', pk=post.pk)
    else:
        form = IngredientsForm(instance=post)
    return render(request, 'blog/post_ingredientedit.html', {'form': form})


def post_ingredientnew(request):
    if request.method == 'POST':
        form = IngredientsForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_ingredientdetail', pk=post.pk)
    else:
        form = IngredientsForm()
    return render(request, 'blog/post_ingredientedit.html', {'form': form})


def new_supper(request):
    if request.method == 'POST':
        form = MenuForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.title = 'ужин'
            # post.date = timezone.now()
            if Menu.objects.all().filter(date__month=timezone.now().month, date__day=timezone.now().day,
                                         date__year=timezone.now().year, title='ужин').count() >= 1:
                post.date = timezone.now() + timedelta(days=1)
            post.save()
            form.save_m2m()
            # post.ingredients()
            return redirect('/')
    else:
        form = MenuForm()
    return render(request, 'blog/supper_edit.html', {'form': form})


def new_breakfast(request):
    args = {}
    args.update(csrf(request))
    i=0
    if request.method == 'POST':
        form = MenuForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            for dish in post:
                for ingredient in dish.ingredients.all:
                    if ingredient > 0 and Ingredient.get(name=ingredient.name).weight - MenuForm(
                            request.POST.cleaned_data['weight']) > 0:
                       ingredient = Ingredient.get(name=ingredient.name).weight - MenuForm(
                            request.POST.cleaned_data['weight'])
                    else:
                        i=i+1
                        args['new_breakfast_error'] =args['new_breakfast_error']+", "+ingredient.name

            if i>0:
                return render_to_response('login.html', args)
            else:
                for dish in post:
                    for ingredient in dish.ingredients.all:
                        if ingredient > 0 and Ingredient.get(name=ingredient.name).weight - MenuForm(
                                request.POST.cleaned_data['weight']) > 0:
                            ingredient = Ingredient.get(name=ingredient.name).weight - MenuForm(
                                request.POST.cleaned_data['weight'])
                            ingredient.save()
            post.title = 'завтрак'

            # post.date = timezone.now()
            if Menu.objects.all().filter(date__month=timezone.now().month, date__day=timezone.now().day,
                                         date__year=timezone.now().year, title='завтрак').count() >= 1:
                post.date = timezone.now() + timedelta(days=1)
            post.save()
            form.save_m2m()
            # post.ingredients()
            return redirect('/')
    else:
        form = MenuForm()
    return render(request, 'blog/breakfast_edit.html', {'form': form})


def new_dinner(request):
    if request.method == 'POST':
        form = MenuForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.title = 'обед'
            # post.date = timezone.now()
            if Menu.objects.all().filter(date__month=timezone.now().month, date__day=timezone.now().day,
                                         date__year=timezone.now().year, title='обед').count() >= 1:
                post.date = timezone.now() + timedelta(days=1)
            post.save()
            form.save_m2m()
            # post.ingredients()
            return redirect('/')
    else:
        form = MenuForm()
    return render(request, 'blog/dinner_edit.html', {'form': form})


def menu_archive(request):
    posts = Menu.objects.all()
    return render(request, 'blog/menu_archive.html', {'posts': posts})


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog.views.dishes_list')


def menu_remove(request, pk):
    post = get_object_or_404(Menu, pk=pk)
    post.delete()
    return redirect('blog.views.menu_archive')


def menu_item_remove(request, **kwargs):
    pk = kwargs.get('pk', "")
    post = get_object_or_404(Menu, pk)
    #pk_url_kwarg = 'item_pk'
    ite = post.items.get(pk=kwargs.get('item_pk', ''))
    #ite = post.items.get(pk=pk_url_kwarg)
    post.items.remove(ite)
    return redirect('blog.views.menu_archive')
