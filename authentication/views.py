from django.shortcuts import render_to_response, redirect, render
from authentication.models import User
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from authentication import forms
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required


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
    permission = Permission.objects.create(codename=codename, name=name, content_type=content_type)
    return permission


def no_permission(request):
    return render(request, 'blog/no_permission.html')


@permission_required('is_admin', login_url='/have_no_permission')
def register(request):
    form = forms.NewUserForm()
    if request.POST:
        form = forms.NewUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            role = request.POST.get('role')
            user = User.objects.create_user(username=username, password=password)
            if role == 'is_admin' or role == 'is_cashier':
                permission = create_permission(role, 'user''role')
            else:
                return redirect('/have_no_permision')
            user.user_permissions.add(permission)
            user.save()
            return redirect('/')
    return render(request, 'register.html', {'form': form})
