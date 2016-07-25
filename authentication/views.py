from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from authentication.models import User, UserProfile
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from authentication import forms
from django.contrib.auth.models import Permission, AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from blog.models import Schedule, Post
from django.db.models import Q
from common.json_warper import is_mobile,json_response
from common.permission import have_permission
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, redirect, render, get_object_or_404

from authentication.models import User, UserProfile
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from authentication import forms
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from blog.models import Schedule, Post
from django.db.models import Q


def login(request):
    args = {}
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if not is_mobile(request):
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
            if user is not None:
                if isinstance(user, AnonymousUser):
                    role = '2'
                elif user.has_perm('blog.can_add'):
                    role = '0'
                elif user.has_perm('blog.can_edit_schedule'):
                    role = '0'
                else:
                    role = '1'
            else:
                role = role = '2'
            return json_response({'role': role})

    else:
        return render_to_response('login.html', args)


def logout(request):
    auth_logout(request)
    return redirect("/")


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


def role_is_not_none(role, form):
    if role is not None:
        return True
    else:
        form.add_error('password', 'Укажите роль')
        return False


def register(request):
    form = forms.NewUserForm()
    if request.POST:
        ensure_permissions()
        form = forms.NewUserForm(request.POST)
        role = request.POST.get('role')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, password=password)
            if role is not None:
                if have_permission(request, ['blog.can_add', 'blog.can_edit_schedule']):
                    if role == 'is_admin' or role == 'is_cashier':
                        if role == 'is_admin':
                            permission = Permission.objects.get(codename='can_add')
                        elif role == 'is_cashier':
                            permission = Permission.objects.get(codename='can_edit_schedule')
                    else:
                        user.delete()
                        return redirect('no_permission')
                    e = UserProfile()
                    e.profile = user
                    e.author = request.user
                    e.save()
                    user.user_permissions.add(permission)
                    user.save()
            if request.user.has_perm('blog.can_add') or request.user.has_perm('blog.can_edit_schedule'):
                return redirect('users.html')
            else:
                return redirect('login.html')
    perm = have_permission(request, ['blog.can_add', 'blog.can_edit_scheduele'])
    return render(request, 'register.html', {'form': form, 'perm': perm})


@permission_required('blog.can_add', raise_exception=True)
def users(request):
    perm1 = Permission.objects.get(codename='can_edit_schedule')
    perm2 = Permission.objects.get(codename='can_add')
    users1 = User.objects.filter(Q(user_permissions=perm1))
    users2 = User.objects.filter(Q(user_permissions=perm2))
    perm = have_permission(request, ['blog.can_add', 'blog.can_edit_scheduele'])
    return render(request, 'users.html', {'users1': users1, 'users2': users2, 'perm':perm})


@permission_required('blog.can_add', raise_exception=True)
def user_remove(request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('users.html')