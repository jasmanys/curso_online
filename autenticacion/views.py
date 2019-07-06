from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

@login_required(login_url='/login/')
def index(request):
    user = request.user
    if user.is_superuser:
        return redirect('/admin/')
    return render(request, 'home/home.html')

# Create your views here.
def login_user(request):
    data = {}
    if request.method == 'POST':
        usuario = request.POST['username']
        contrasena = request.POST['password']
        data['username'] = usuario
        data['password'] = contrasena
        if '@' in usuario:
            if User.objects.filter(email = usuario).exists():
                us=""
                us = User.objects.get(email = usuario).username
                user = authenticate(username=us, password = contrasena)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        data['user'] = user
                        return redirect('/')
                    else:
                        return redirect('/login/?error=no-active')
                else:
                    return redirect('/login/?error=pass-error')
            else:
                return redirect('/login/?error=email-error')
        else:
            if User.objects.filter(username=usuario).exists():
                user = authenticate(username=usuario, password=contrasena)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        data['user'] = user
                        return redirect('/')
                    else:
                        return redirect('/login/?error=no-active')
                else:
                    return redirect('/login/?error=pass-error')
            else:
                return redirect('/login/?error=username-error')
    else:
        if 'error' in request.GET:
            data['error']=request.GET['error']
        return render(request, 'login/login.html', data)

def logout_user(request):
    logout(request)
    return redirect('/')