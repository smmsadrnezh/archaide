import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render


# from software_architect_aide.forms import UserRegisterForm


def sign_in(request):
    if request.method == "POST":
        user = authenticate(username=User.objects.get(email=request.POST.get('email', '')).username,
                            password=request.POST.get('password', ''))
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'sign_in.html', {'success': False})
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request, 'sign_in.html', {'success': True})


def sign_out(request):
    logout(request)
    return redirect(sign_in)


@login_required(login_url='/')
def dashboard(request):
    context = {'': '', }
    return render(request, 'dashboard_home.html', context)


@login_required(login_url='/')
def instantiate(request):
    context = {'': '', }
    return render(request, 'dashboard_instantiate.html', context)


@login_required(login_url='/')
def tradeoff(request):
    context = {'': '', }
    return render(request, 'dashboard_tradeoff.html', context)


@login_required(login_url='/')
def evolution(request):
    context = {'': '', }
    return render(request, 'dashboard_evolution.html', context)


def register(request):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password2 != password:
            return render(request, 'register.html', {'match_password': False})

        # TODO: get user from database
        if user is not None:
            return render(request, 'register.html', {'duplicate_user': True})

        User.objects.create_user(username=email, email=email, password=password)
        return redirect('sign_in')
    else:
        return render(request, 'register.html', {'success': True})
