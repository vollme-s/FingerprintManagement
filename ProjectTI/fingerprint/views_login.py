from django.shortcuts import render_to_response, redirect

from django.contrib import auth
from django.contrib.auth.models import User
from django.core.context_processors import csrf


def login(request):
    priv = request.GET.get('priv', '')
    c = {'priv': priv, }
    c.update(csrf(request))
    return render_to_response('fingerprint/login/login.html', c)


def loggedin(request):
    return render_to_response('fingerprint/login/loggedin.html',
                              {'full_name': request.user.username})

def invalid_login(request):
    return render_to_response('fingerprint/login/invalid_login.html')


def auth_view(request):
    priv = request.GET.get('priv', '')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        if priv == 'Admin':
            if user.is_staff:
                return redirect('/fingerprint/home_admin/')
            else:
                return redirect('/fingerprint/accounts/invalid/')
        else:
            return redirect('/fingerprint/home_user/')
    else:
        return redirect('/fingerprint/accounts/invalid/')


def logout(request):
    auth.logout(request)
    return redirect('/fingerprint/accounts/login/')


def registration(request): 
    c = {}
    c.update(csrf(request))
    return render_to_response('fingerprint/login/registration.html', c)


def registrate_user(request):
    username = request.POST.get('username', '')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')

    if username and password and email:
        user = User.objects.create_user(username=username, email=email,
             first_name=first_name, last_name=last_name, password=password)
        if user:
            
            message = "Your registration has been accepted!"
            context = {'message': message,
                       'username': username,}    
            return render_to_response('fingerprint/login/info.html', context)
        else:
            return redirect('/fingerprint/accounts/loggedin/')
    else:
        return redirect('/fingerprint/accounts/invalid/')