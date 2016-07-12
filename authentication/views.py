from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, redirect, render, get_object_or_404

from authentication.forms import NewUserForm
from authentication.models import User, UserProfile
from django.template.context_processors import csrf, request
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from authentication import forms
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from blog.models import Schedule, Post
from django.db.models import Q

def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('/')
            else:
                args['login_error'] = "Пользователь не активен"
                return render_to_response('login.html', args)
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)


def logout(request):
    auth_logout(request)
    return redirect("/")


def create_permission(codename, name):
    content_type = ContentType.objects.get_for_model(User)
    permission = Permission.objects.create(codename='can_add', name='can add a user', content_type=content_type)
    return permission


def no_permission(request):
    return render(request, 'blog_templates/no_permission.html')


def ensure_permissions():
    content_type = ContentType.objects.get_for_model(Post)
    content_type1 = ContentType.objects.get_for_model(Schedule)
    try:
        Permission.objects.create(codename='can_add', name='can add a user', content_type=content_type)
    except Exception:
        pass
    try:
        Permission.objects.create(codename='can_edit_schedule', name='can edit scheudle', content_type=content_type1)
    except:
        pass


@permission_required('blog.can_add', raise_exception=True)
def register(request):
    form = forms.NewUserForm()
    if request.POST:
        ensure_permissions()
        form = forms.NewUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            role = request.POST.get('role')
            user = User.objects.create_user(username=username, password=password)
            print('ghghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
            if role == 'is_admin' or role == 'is_cashier':
                if role == 'is_admin':
                    permission = Permission.objects.get(codename='can_add')
                elif role == 'is_cashier':
                    permission = Permission.objects.get(codename='can_edit_schedule')
            else:
                return redirect('/auth/no_permision')
            e = UserProfile()
            e.profile = user
            e.author = request.user
            e.save()
            user.user_permissions.add(permission)

            user.save()

            return redirect('/')
    return render(request, 'register.html', {'form': form})

def users(request):
    perm1 = Permission.objects.get(codename='can_edit_schedule')
    perm2 = Permission.objects.get(codename='can_add')
    users1 = User.objects.filter(Q(user_permissions=perm1))
    users2 = User.objects.filter(Q(user_permissions=perm2))
    return render(request, 'users.html', {'users1': users1, 'users2':users2})


@permission_required('blog.can_add', raise_exception=True)
def user_remove(request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('authentication.views.user')
