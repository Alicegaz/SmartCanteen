from django.contrib.auth.decorators import user_passes_test

from blog.forms import PostForm, IngredientsForm, MenuForm
from .models import Post, Ingredient
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
#from .forms import PostForm, IngredientsForm, MenuForm
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.template.context_processors import csrf
from django.core import serializers

def post_list(request):
    json = request.GET.get('json')
    posts = Post.objects.all().order_by('published_date')
    if not json:
        posts = Post.objects.all().order_by('published_date')
        return render(request, 'blog/post_list.html', {'posts': posts})
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

#@user_passes_test(user.is_stuff, '/have_no_permission')
def post_admin(request):
    if request.user.is_superuser:

        args = {}
        args.update(csrf(request))
        args['username'] = auth.get_user(request).is_superuser
        return render(request, 'blog/post_admin.html', args)
    else:
        return HttpResponse("У вас нет прав администратора")


#def post_ingredientlist(request):
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
            post.save()
            form.save_m2m()
            post_numder = post.pk
            for ing in request.POST.getlist('ingredients'):
                theing = Ingredient.objects.get(pk=ing)
                post.ingredients.add(theing.id)

            messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
            # return HttpResponseRedirect(instance.get_absolute_url())
            context = {
                "title": post.title,
                "instance": post,
                "form": form,
            }
            return render(request, 'blog/post_edit.html', context)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {'form': form, 'username': auth.get_user(request).is_superuser})


def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
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
    return render(request, 'blog/post_edit.html', {'form': form, 'username': auth.get_user(request).is_superuser})



def new_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            # post.ingredients()
            return redirect('post_list')
    else:
        form = MenuForm()
    return render(request, 'blog/new_menu.html', {'form': form, 'username': auth.get_user(request).is_superuser})



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
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            # post_numder = post.pk
            messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
            # return HttpResponseRedirect(instance.get_absolute_url())
            context = {
                "title": post.name,
                "instance": post,
                "form": form,
            }
            return render(request, 'blog/post_ingredientedit.html', context)
    else:
        form = IngredientsForm(instance=post)
    return render(request, "blog/post_ingredientedit.html", {'form': form, 'username': auth.get_user(request).is_superuser})


def post_ingredientnew(request):
    if request.method == 'POST':
        form = IngredientsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_ingredientdetail', pk=post.pk)
    else:
        form = IngredientsForm()
    return render(request, 'blog/post_ingredientedit.html',
                  {'form': form, 'username': auth.get_user(request).is_superuser})
