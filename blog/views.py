from .models import Post, Ingredient
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, IngredientsForm
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    posts = Post.objects.all().order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk=None):
    instance = get_object_or_404(Post, pk=pk)
    ingredientss = instance.ingredients.all()
    context = {
        "title": instance.title,
        "instance": instance,
        "ingredientss": ingredientss,

    }
    return render(request, 'blog/post_detail.html', context)


def post_admin(request):
    return render(request, 'blog/post_admin.html')


def post_ingredientslist(request):
    ingredientss = Ingredient.objects.all().order_by('published_date')
    return render(request, 'blog/post_ingredientlist', {'ingredientss': ingredientss})


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
    return render(request, "blog/post_edit.html", {'form': form})


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
    return render(request, 'blog/post_edit.html', {'form': form})


def post_ingredientdetail(request, pk1=None):
    instance1 = get_object_or_404(Ingredient, pk1=pk1)
    context = {
        "title": instance1.name,
        "instance": instance1,

    }
    return render(request, 'blog/post_detail.html', context)


def post_ingredientedit(request):
    instance = get_object_or_404(Ingredient, id=id)
    form = IngredientsForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.name,
        "instance": instance,
        "form": form,
    }
    return render(request, "blog/post_ingredientedit.html", context)


def post_ingredientnew(request):
    if request.method == 'POST':
        form1 = IngredientsForm(request.POST, request.FILES)
        if form1.is_valid():
            post = form1.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_ingredientdetail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_ingredientedit.html', {'form': form})
