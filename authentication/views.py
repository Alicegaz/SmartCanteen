from django.shortcuts import render_to_response, redirect, render
from authentication.models import User
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from authentication import forms
from django.contrib.auth.decorators import user_passes_test


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


def user_is_stuff(user):
    return user.is_authenticated() and user.is_staff


@user_passes_test(user_is_stuff, '/have_no_permision')
def register(request):
    form = forms.NewUserForm()
    if request.POST:
        form = forms.NewUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            is_admin = None
            is_cashier = None
            user = User.objects.create_user(username=username, password=password)
            user.user_permissions.add()
            user.save()
            return redirect('/')
    return render(request, 'register.html', {'form': form})


