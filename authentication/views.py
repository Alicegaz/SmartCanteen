from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, redirect, render
from authentication.models import User
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from authentication import forms
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from blog.models import Schedule, Post


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


@permission_required('blog.can_add', raise_exception=True)
def register(request):
    form = forms.NewUserForm()
    content_type = ContentType.objects.get_for_model(Post)
    content_type1 = ContentType.objects.get_for_model(Schedule)
    if Permission.objects.all().count() == 0:
        Permission.objects.create(codename='can_add', name='can add a user', content_type=content_type)
        Permission.objects.create(codename='can_edit_schedule', name='can edit scheudle', content_type=content_type1)
    if request.POST:
        form = forms.NewUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            role = request.POST.get('role')
            user = User.objects.create_user(username=username, password=password)
            if role == 'is_admin' or role == 'is_cashier':
                if role == 'is_admin':
                   permission = Permission.objects.get(codename='can_add')
                elif role == 'is_cashier':
                   permission = Permission.objects.get(codename='can_edit_schedule')
            else:
                return redirect('/auth/no_permision')
            user.user_permissions.add(permission)
            user.save()
            return redirect('/')
    return render(request, 'register.html', {'form': form})
