import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render


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
